# Symptom Specialist Agents: Beginner Build and Launch Guide

You do not need to write any code. Every file is already written and tested in this folder. Your job is to
(1) run it on your computer, (2) put it on the internet, (3) run a careful pilot.

Estimated time: 2 to 3 hours for steps 1 to 5, then a 3 to 4 week pilot.

---------------------------------------------------------------------

## What you are building

A website where a person types their symptoms. Behind the scenes:

1. Safety rules check for emergencies or self-harm first (no AI involved, instant).
2. Four specialist AI agents (Cardiology, Neurology, Gastroenterology, Rheumatology) review the case AT THE SAME TIME.
   Each returns: a relevance score, a differential diagnosis (ranked possible causes, including "must not miss" ones),
   a small decision tree (questions a doctor would ask next), red flags, suggested tests and next steps.
3. A Coordinator agent merges the four opinions into one ranked list, one urgency level and plain-language next steps.
4. A safety net makes sure the AI can never downgrade an emergency that the rules caught.

## What every file does

| File | What it does | Do you edit it? |
|---|---|---|
| `requirements.txt` | List of software libraries the server needs | No |
| `.env.example` | Template for your secret settings (API key etc.) | Copy it to `.env` and fill in |
| `.gitignore` | Tells GitHub to ignore secrets and junk | No |
| `app/config.py` | Reads the settings (model name, limits, timeouts) | Rarely |
| `app/schemas.py` | Defines the form fields and turns them into text for the agents | No |
| `app/triage.py` | Emergency and self-harm keyword rules, plus the help messages | Later, with a clinician |
| `app/agents.py` | The job descriptions (prompts) of the 4 specialists and the coordinator, and the code that calls Grok | Yes, to tune the AI |
| `app/mock.py` | Fake answers for testing without an API key | No |
| `app/orchestrator.py` | Runs the 4 specialists in parallel, then the coordinator, then the safety net | No |
| `app/main.py` | The web server: serves the page, receives the form, access code, rate limit | No |
| `static/index.html` | The whole website (design, form, results display) | Yes, for wording and design |

---------------------------------------------------------------------

## STEP 1: Install the tools (one time, about 20 minutes)

1. **Python**: go to https://www.python.org/downloads and install the latest Python 3.11 or newer.
   On Windows, on the first installer screen TICK the box "Add python.exe to PATH". This is the most common mistake.
2. **VS Code** (a free editor): https://code.visualstudio.com
3. Unzip the project folder `symptom-ai` somewhere easy, for example your Desktop.
4. Open VS Code, choose File > Open Folder, and pick the `symptom-ai` folder.
5. Open the built-in terminal: menu Terminal > New Terminal. A panel opens at the bottom. All commands below are typed there.

## STEP 2: Run it on your computer in DEMO mode (no API key, no cost)

Type these one at a time, pressing Enter after each.

**Mac:**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

**Windows (use the Command Prompt terminal; in VS Code click the small arrow next to + in the terminal panel and choose "Command Prompt"):**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Now open the new file `.env` in VS Code and change the line `DEMO_MODE=false` to `DEMO_MODE=true`. Save (Ctrl+S or Cmd+S).

Start the server:
```
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 in your browser. You should see the website with a yellow "Demo mode" note.
Fill the form and click Analyse. After a few seconds you see sample results. This proves the website works.
To stop the server, click in the terminal and press Ctrl+C.

## STEP 3: Switch on real AI with Grok

1. Go to https://console.x.ai/ and create an account.
2. Create an API key and configure API billing/credits in the xAI console.
3. In `.env`, remove the old `ANTHROPIC_API_KEY` and `MODEL_NAME` entries, set `XAI_API_KEY` to your xAI key,
   and set `DEMO_MODE=false`. Keep the key private.
4. Leave `XAI_MODEL_NAME=grok-4.7` unless you have selected another model available to your API account.
   See the current [xAI model list](https://docs.x.ai/developers/models).
5. Set a usage limit in the xAI console if available, then save `.env`.
6. Stop the server (Ctrl+C) and start it again with `uvicorn app.main:app --reload`.
7. Test with these inputs and check the behaviour:

| Test input | What you should see |
|---|---|
| 45 year old man, pressure in the chest when climbing stairs for 3 days | Red emergency warning, cardiology scores high |
| 30 year old woman, throbbing headache on one side with light sensitivity and nausea | Neurology high, migraine near the top |
| 38 year old man, burning upper stomach pain after meals, worse at night | Gastroenterology high (GERD, ulcer) |
| 52 year old woman, stiff swollen finger joints every morning for an hour | Rheumatology high |
| 28 year old, "I feel like I want to die" | No diagnosis, only the crisis help message |
| 35 year old, mild sore throat for one day | Low relevance everywhere, routine or self-care |

If a specialist is unrelated, its relevance bar should be short. That is correct behaviour.

## STEP 4: Put the code on GitHub (about 15 minutes)

GitHub is a website that stores your code so the hosting service can read it.

1. Create a free account at https://github.com.
2. Click the + at the top right, New repository. Name it `symptom-ai`, choose **Private**, click Create repository.
3. On the new page click "uploading an existing file".
4. Open your `symptom-ai` folder in your file manager. Select and drag these into the browser: the `app` folder,
   the `static` folder, `requirements.txt`, `.gitignore`, `.env.example`, `GUIDE.md`.
   **DO NOT upload** the `.env` file or the `venv` folder. `.env` contains your secret key.
   (Mac hides files starting with a dot: press Cmd+Shift+. in Finder to show them.)
5. Click "Commit changes".

## STEP 5: Launch it on the internet with Render (about 20 minutes)

1. Create a free account at https://render.com, choose "Sign in with GitHub" and allow access to your repository.
2. Click New + > Web Service, select your `symptom-ai` repository.
3. Fill in:
   - Name: `symptom-ai` (this becomes part of your web address)
   - Region: choose the one closest to your users (Singapore for India)
   - Branch: `main`
   - Runtime / Language: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Instance type: Free for first tests. For a real pilot choose Starter (the free plan "sleeps" after about 15 minutes
     of no visitors and the next visitor waits roughly a minute).
4. Open "Advanced" and add Environment Variables (this is where secrets live, not in the code):
   - `XAI_API_KEY` = your xAI key
   - `XAI_MODEL_NAME` = `grok-4.7`
   - `ACCESS_CODE` = a password of your choice (share it only with pilot users)
   - `RATE_LIMIT_PER_HOUR` = `8`
   - `PYTHON_VERSION` = `3.11.11`
   - Set Health Check Path to `/health`.
5. Click Create Web Service. Wait 3 to 5 minutes. When the log says the service is live, open the address
   `https://symptom-ai.onrender.com` (yours will show at the top of the page).
6. Repeat the 6 tests from Step 3 on the live site, on your phone as well.

To change anything later: edit the file on GitHub (open file, pencil icon, commit). Render redeploys automatically.

---------------------------------------------------------------------

## STEP 6: Make it safe before real users (do not skip)

This tool deals with health, so treat this as part of the product.

1. **Clinician review.** Ask 1 or 2 doctors (ideally one general physician and one specialist) to run 30 to 50 realistic
   cases and mark each result: Was the urgency right? Was a dangerous cause missed? Was anything misleading?
   Keep a spreadsheet. Fix prompts in `app/agents.py` and emergency phrases in `app/triage.py` based on their feedback.
   Aim for zero missed emergencies in your test set before inviting outsiders.
2. **Wording.** Never describe it as "diagnosing". Use "possible causes" and "prepare for your doctor visit".
   The disclaimers in the page already do this. Keep them.
3. **Privacy.** The server does not store symptom text or log it. xAI processes the text to generate results; review its current
   data and privacy terms. API requests disable response storage, but this does not replace checking provider policies.
   Add a short privacy page before a public launch. Depending on your users, laws such as India's DPDP Act, GDPR or HIPAA
   may apply, and software that suggests diagnoses can count as a regulated medical device in some countries.
   Talk to a lawyer or regulatory adviser before any paid or public launch. This guide is not legal advice.
4. **Cost control.** One analysis makes 5 AI calls (4 specialists plus the coordinator). Watch usage and billing in the xAI console
   during the pilot, and check the [current model pricing](https://docs.x.ai/developers/models).
5. **Access control.** Keep `ACCESS_CODE` on during the pilot.

## STEP 7: Pilot, then public MVP launch

| Week | Goal |
|---|---|
| 1 | Steps 1 to 5 done, live on a private link, you test it yourself |
| 2 | Clinician review of 30 to 50 cases, fix prompts and rules |
| 3 | Invite 20 to 50 friendly users with the access code. Ask: Was it understandable? Did you trust it? What would you do next? |
| 4 | Fix top issues, add privacy page, decide go or no-go for wider launch |

Numbers to track in a simple sheet: number of analyses, how many ended in an emergency or urgent result, how many users said
the result was clear (ask them), errors seen, API cost per analysis.

To go public: remove `ACCESS_CODE` (or keep it and hand it out), buy a domain name (optional) and attach it in
Render under Settings > Custom Domains, and keep the rate limit on.

---------------------------------------------------------------------

## Changing things later

- **Change the AI model:** change `XAI_MODEL_NAME` in Render Environment Variables.
- **Tune medical behaviour:** edit the text inside `SPECIALIST_SYSTEM_PROMPT` and `SYNTHESIS_SYSTEM_PROMPT` in `app/agents.py`.
- **Add a specialist (for example Pulmonology):** in `app/agents.py` copy one block in the `SPECIALISTS` list, change `id`, `title`, `scope`.
  In `static/index.html` add one more `<div class="agent-row">` line in the progress section and mention it in the page intro.
- **Change colours and fonts:** edit the `:root { ... }` block at the top of `static/index.html`.
- **Add emergency phrases:** edit `EMERGENCY_PATTERNS` in `app/triage.py`.

## If something goes wrong

| Problem | Fix |
|---|---|
| `python` or `pip` not recognised (Windows) | Reinstall Python and tick "Add python.exe to PATH", reopen VS Code |
| `uvicorn` not recognised | You forgot to activate the venv: run the `source venv/bin/activate` or `venv\Scripts\activate` line again |
| Page says "Server is not configured yet" | `XAI_API_KEY` missing or DEMO_MODE not set; check `.env` (local) or Environment Variables (Render) |
| "Access code is missing or incorrect" | Type the exact `ACCESS_CODE` in the access code field |
| "Something went wrong while analysing" | Check Render Logs. Usually a wrong xAI API key, insufficient credits, or a wrong `XAI_MODEL_NAME` |
| Render build fails | Open the log; confirm `requirements.txt` is in the repository root and the Start Command is exactly as above |
| First visit very slow on Render | Free plan was asleep. Use the Starter plan for pilots |

## After the MVP: enhancement ideas (for later)

Follow-up questions in a chat style, user accounts and saved history, doctor-facing view, more specialties,
multilingual support (Hindi, Telugu), retrieval from trusted clinical guidelines, a formal evaluation set with scoring,
streaming each agent's result as it finishes, analytics dashboard, and a doctor-referral handoff.
