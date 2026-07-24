# Travel Agent MVP

A small multi-agent travel-planning app. You describe a trip in plain language; a root agent extracts your requirements, delegates destination research and itinerary building to two specialist agents, and returns one structured plan.

Built with Google ADK + Gemini (via Vertex AI), FastAPI, Streamlit, and SQLite. See `docs/product-contract.md` for the full behavioral contract and `docs/architecture.html` for a visual diagram (open it in a browser).

## What it does

- Interprets a natural-language trip request (origin, destination, duration, budget, travellers, interests, pace).
- Recommends a destination if you don't name one.
- Produces: request summary, assumptions, destination guidance, day-by-day itinerary, estimated budget, practical notes, and a price/availability disclaimer.
- Supports follow-ups in the same conversation ("make day two more relaxed") without losing earlier context.
- Keeps separate conversations fully isolated from each other.
- Survives an app restart — conversations are saved to SQLite, not memory.

## What it does not do

- No real bookings, payments, or live flight/hotel prices — every cost is a labelled estimate.
- No authentication — anyone with access to the app can start a session.
- No visa/legal advice as fact.
- SQLite is for local development only, not a production data store.

## Architecture

```
Streamlit UI  --HTTP-->  FastAPI  -->  agent_runner (Runner + DatabaseSessionService)
                                            |
                                        root_agent (validates duration itself)
                                       /            \
                          destination_agent      itinerary_agent (uses allocate_budget tool)
                                       \            /
                                        Gemini (Vertex AI)

SQLite (data/travel_agent.db) <-- sessions & conversation history
```

Full diagram with notes: `docs/architecture.html`.

## Setup

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), and a GCP project with Vertex AI enabled.

```bash
# 1. Python environment
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# 2. GCP auth (one-time)
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com
```

Copy `.env.example` to `.env` and fill in your project:

```
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## Running it

Two processes, two terminals:

```bash
# Terminal 1 — backend
uv run uvicorn backend.api.main:app --reload

# Terminal 2 — frontend
uv run streamlit run frontend/streamlit_app.py
```

Streamlit opens a browser tab automatically. Try a sample prompt from the sidebar, then a follow-up message, then "Start new conversation" to confirm sessions are independent.

## Example prompts

From `backend/tests/evaluation_cases.md`:

- "Plan a four-day Goa trip from Delhi for two people under ₹40,000. We like beaches, local food, and a relaxed pace."
- "Suggest and plan a three-day trip from Bengaluru under ₹25,000 for one person. I enjoy nature and quiet places."
- "Plan a trip to Jaipur." *(missing duration — should ask a clarifying question, not fabricate a plan)*
- "Plan a seven-day international trip from Mumbai for two people under ₹20,000." *(should flag the budget as unrealistic)*
- "Plan a five-day Kerala trip for a family of four." then "Make day three less tiring and reduce expensive activities." *(follow-up should modify, not restart)*

## Known limitations

- Vertex AI free-tier/trial projects can have low per-minute request quotas; a single turn makes 3+ chained model calls (root + destination + itinerary), so `429 RESOURCE_EXHAUSTED` errors are possible under rapid back-to-back messages. See Cloud Console → Vertex AI API → Quotas.
- Currency formatting and a local destination reference dataset (both listed in `plan.md` Step 6) were deliberately skipped as low-value for this MVP.
- Comparative region/sub-destination analysis (e.g. "compare these 3 islands") and live flight/hotel price + review fetching are noted as future extensions in `plan.md` section 13, not implemented here.
- No automated test suite (pytest) yet — testing so far is manual, via the scripts in `backend/tests/`.

## Project structure

```
backend/
  api/           FastAPI app (main.py, schemas.py)
  services/      agent_runner.py — singleton Runner + session service
  travel_agent/  root_agent, destination_agent, itinerary_agent + prompts/
  tools/         deterministic Python tools (budget, duration)
  tests/         manual test scripts + evaluation_cases.md
frontend/
  streamlit_app.py
data/
  travel_agent.db  (gitignored, created on first run)
docs/
  product-contract.md, architecture.html
```
