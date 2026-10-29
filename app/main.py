"""The web server. It serves the website and one API endpoint: /api/analyze"""
import asyncio
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import config
from .orchestrator import analyze
from .schemas import PatientInput, format_patient
from .triage import run_triage

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Symptom Specialist Agents (MVP)", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- very simple rate limiter (remembers requests per IP address in memory) ---
_hits: dict = {}


def check_rate_limit(ip: str) -> None:
    now = time.time()
    recent = [t for t in _hits.get(ip, []) if now - t < 3600]
    if len(recent) >= config.RATE_LIMIT_PER_HOUR:
        raise HTTPException(429, "You have reached the hourly limit. Please try again later.")
    recent.append(now)
    _hits[ip] = recent


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/config")
def public_config():
    return {"needs_code": bool(config.ACCESS_CODE), "demo": config.DEMO_MODE}


@app.post("/api/analyze")
async def analyze_endpoint(patient: PatientInput, request: Request):
    if config.ACCESS_CODE and patient.access_code != config.ACCESS_CODE:
        raise HTTPException(401, "Access code is missing or incorrect.")
    if not config.DEMO_MODE and not config.XAI_API_KEY:
        raise HTTPException(500, "Server is not configured yet (missing XAI_API_KEY).")

    check_rate_limit(client_ip(request))

    triage = run_triage(format_patient(patient))
    if triage["level"] == "crisis":  # skip diagnosis entirely, show help
        return {"triage": triage, "specialists": [], "synthesis": None}

    try:
        return await asyncio.wait_for(analyze(patient, triage), timeout=config.OVERALL_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        raise HTTPException(504, "The analysis took too long. Please try again.")
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"[server-error] {type(exc).__name__}: {exc}")  # never logs patient text
        raise HTTPException(502, "Something went wrong while analysing. Please try again.")


@app.exception_handler(HTTPException)
async def http_exc_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
