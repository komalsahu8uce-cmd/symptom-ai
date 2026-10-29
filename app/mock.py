"""Fake answers used when DEMO_MODE=true, so you can test the website with no API key and no cost."""
import asyncio


async def mock_specialist(spec: dict) -> dict:
    await asyncio.sleep(1.2)
    return {
        "id": spec["id"], "title": spec["title"], "relevance": 6,
        "summary": f"(DEMO) Sample opinion from the {spec['title']}. Real AI answers appear when DEMO_MODE is off.",
        "differential": [
            {"condition": "Sample condition A", "likelihood": "moderate", "must_not_miss": False,
             "reasoning": "This is placeholder reasoning for testing the layout.",
             "supporting": ["Sample supporting detail"], "against_or_missing": ["Sample missing detail"]},
            {"condition": "Sample dangerous condition B", "likelihood": "low", "must_not_miss": True,
             "reasoning": "Placeholder: dangerous but less likely, so it must be ruled out.",
             "supporting": ["Sample detail"], "against_or_missing": ["Sample detail"]},
        ],
        "decision_tree": [{"question": "Sample question to ask next?",
                           "if_yes": "Points toward condition A.", "if_no": "Points away from condition A."}],
        "red_flags": ["Sample red flag: sudden severe worsening"],
        "suggested_tests": ["Sample test: blood test"],
        "next_steps": ["Sample step: book a visit with a doctor"],
    }


async def mock_synthesis() -> dict:
    await asyncio.sleep(0.8)
    return {
        "urgency": "see_doctor_soon",
        "urgency_reason": "(DEMO) Placeholder reason for this urgency level.",
        "plain_summary": "(DEMO) This is a sample summary. Turn off DEMO_MODE to get real AI analysis.",
        "top_possibilities": [{"condition": "Sample condition A", "likelihood": "moderate",
                               "supported_by": ["Cardiology", "Neurology"], "why": "Placeholder explanation."}],
        "recommended_doctor": "General Physician",
        "next_steps": ["Sample next step one", "Sample next step two"],
        "questions_to_answer": ["Sample question: does it get worse with movement?"],
        "go_to_emergency_if": ["Sample: sudden severe pain"],
        "disagreements_or_gaps": ["Sample gap: no vital signs available"],
    }
