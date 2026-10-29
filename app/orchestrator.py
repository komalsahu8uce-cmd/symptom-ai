"""The 'conductor': runs the four specialists at the same time, then the coordinator."""
import asyncio

from . import config
from .agents import SPECIALISTS, run_specialist, run_synthesizer
from .mock import mock_specialist, mock_synthesis
from .schemas import PatientInput, format_patient

URGENCY_ORDER = ["self_care", "routine", "see_doctor_soon", "urgent_24h", "emergency"]


async def analyze(patient: PatientInput, triage: dict) -> dict:
    patient_text = format_patient(patient)

    # Step 1: all four specialists work AT THE SAME TIME
    if config.DEMO_MODE:
        specialists = await asyncio.gather(*[mock_specialist(s) for s in SPECIALISTS])
    else:
        specialists = await asyncio.gather(*[run_specialist(s, patient_text) for s in SPECIALISTS])

    working = [s for s in specialists if "error" not in s]
    if not working:
        raise RuntimeError("All specialists failed")

    # Step 2: coordinator merges their opinions
    if config.DEMO_MODE:
        synthesis = await mock_synthesis()
    else:
        synthesis = await run_synthesizer(patient_text, working)

    # Safety net #2: if our rules saw an emergency, never let the AI downgrade it
    if triage["level"] == "emergency":
        if URGENCY_ORDER.index(synthesis.get("urgency", "routine")) < URGENCY_ORDER.index("emergency"):
            synthesis["urgency"] = "emergency"
            synthesis["urgency_reason"] = (
                "Your description includes warning signs that can be serious: "
                + ", ".join(triage["reasons"]) + ". " + synthesis.get("urgency_reason", "")
            )

    return {"triage": triage, "specialists": list(specialists), "synthesis": synthesis}
