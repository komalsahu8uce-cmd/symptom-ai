"""Safety net #1: simple rules that run BEFORE any AI.
If the text contains emergency phrases we show an emergency warning immediately,
and for self-harm phrases we skip the diagnosis and show crisis help instead."""
import re

CRISIS_PATTERNS = [
    r"suicid", r"kill myself", r"end my life", r"want to die", r"self[- ]harm",
    r"hurt myself", r"don'?t want to live", r"take my own life",
]

EMERGENCY_PATTERNS = {
    r"chest (pain|pressure|tightness|discomfort)|chest (feels |is )?(tight|heavy)|(pressure|tightness|heaviness|pain|squeezing) (in|on|across) (my |the )?chest|crushing|pain.{0,20}(left arm|jaw)": "Chest pain or pressure",
    r"(can'?t|cannot|unable to) breathe|difficulty breathing|struggling to breathe|gasping": "Severe breathing difficulty",
    r"face (is )?droop|slurred speech|sudden(ly)? (weak|numb)|one side of (my )?(body|face)": "Possible stroke signs",
    r"worst headache|thunderclap|sudden severe headache": "Sudden severe headache",
    r"lost consciousness|loss of consciousness|passed out|fainted|blacked out|unconscious": "Loss of consciousness",
    r"seizure|convuls": "Seizure",
    r"vomit(ing|ed)? blood|blood in (my )?vomit|coughing (up )?blood|black (tarry )?stool|tarry stool|blood in (my )?stool|rectal bleeding": "Possible serious bleeding",
    r"throat (is )?(closing|swelling)|swelling of (the )?(throat|tongue|lips)|anaphyla": "Possible severe allergic reaction",
    r"stiff neck.{0,40}fever|fever.{0,40}stiff neck": "Fever with stiff neck",
    r"overdos|poison": "Possible overdose or poisoning",
}

EMERGENCY_MESSAGE = (
    "Some of what you describe can be a medical emergency. Do not wait for this tool. "
    "Call your local emergency number now (India: 112 or 108; US: 911; UK: 999) "
    "or go to the nearest emergency room."
)

CRISIS_MESSAGE = (
    "You do not have to go through this alone. Please reach out to someone right now. "
    "India: Tele-MANAS 14416 (free, 24x7) or call 112. US: call or text 988. "
    "UK and Ireland: Samaritans 116 123. If you are in immediate danger, call your local emergency number. "
    "If you can, tell a family member or friend how you are feeling today."
)


def run_triage(text: str) -> dict:
    t = text.lower()
    for pat in CRISIS_PATTERNS:
        if re.search(pat, t):
            return {"level": "crisis", "reasons": ["Thoughts of self-harm"], "message": CRISIS_MESSAGE}
    reasons = [label for pat, label in EMERGENCY_PATTERNS.items() if re.search(pat, t)]
    if reasons:
        return {"level": "emergency", "reasons": reasons, "message": EMERGENCY_MESSAGE}
    return {"level": "none", "reasons": [], "message": ""}
