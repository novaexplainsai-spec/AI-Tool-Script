# AI Tool Script Pipeline

Small automation that runs on a schedule via GitHub Actions:

1. Fetches trending AI/SaaS tool launches from Product Hunt (free API)
2. Picks the first one you haven't covered yet
3. Drafts a video script for it using Groq's free-tier LLM API
4. Saves the draft to `output/scripts/` and commits it back to the repo

This produces a **draft only**. You still need to actually test the tool and
add your own notes/opinion before recording — see `prompts/starter_prompt.txt`.

## Setup

1. Create a Product Hunt developer token: https://www.producthunt.com/v2/oauth/applications
2. Create a free Groq API key: https://console.groq.com/keys
3. In your GitHub repo: Settings → Secrets and variables → Actions → add:
   - `PRODUCTHUNT_TOKEN`
   - `GROQ_API_KEY`
4. (Local testing only) copy `.env.example` to `.env` and fill in the values,
   then `pip install -r requirements.txt` and `python main.py`

## Files

- `fetch_tools.py` — pulls trending tools from Product Hunt
- `generate_script.py` — drafts a script via Groq
- `main.py` — orchestrates both, run manually or by the workflow
- `.github/workflows/pipeline.yml` — the scheduled automation
- `prompts/starter_prompt.txt` — paste into a new LLM chat to polish a draft
- `output/scripts/` — where drafts land
- `output/covered_tools.json` — tracks what you've already made videos about
