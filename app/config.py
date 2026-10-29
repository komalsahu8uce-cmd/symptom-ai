"""All settings live here. Values come from the .env file (local) or from
Render's Environment Variables (live site)."""
import os
from pathlib import Path


def load_dotenv():
	"""Load basic KEY=VALUE entries from the project's .env file."""
	env_file = Path(__file__).resolve().parent.parent / ".env"
	if not env_file.is_file():
		return

	for line in env_file.read_text(encoding="utf-8").splitlines():
		line = line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		key, value = key.strip(), value.strip()
		if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
			value = value[1:-1]
		if key:
			os.environ.setdefault(key, value)

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY", "").strip()
XAI_MODEL_NAME = os.getenv("XAI_MODEL_NAME", "grok-4.7").strip()
DEMO_MODE = os.getenv("DEMO_MODE", "false").strip().lower() == "true"
ACCESS_CODE = os.getenv("ACCESS_CODE", "").strip()
RATE_LIMIT_PER_HOUR = int(os.getenv("RATE_LIMIT_PER_HOUR", "8"))

# Each specialist answer can be up to this many tokens (roughly 0.75 words each).
MAX_TOKENS_SPECIALIST = 2500
MAX_TOKENS_SYNTHESIS = 2500

# If the whole analysis takes longer than this many seconds, we stop and show an error.
OVERALL_TIMEOUT_SECONDS = 120
