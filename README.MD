# B2B Founder LinkedIn Content Agent (NB Media Task Execution)

An automated, asynchronous multi-agent system built to track cutting-edge tech industry news, execute in-depth web research, and synthesize viral LinkedIn content in the exact brand voice and visual footprint of Nikit Bassi (Founder of NB Media)[cite: 1].

## Completed Deliverables Matrix
* **Task 1: Writing Style Training (2 Pts):** Executed via deep linguistic analysis and Few-Shot In-Context learning utilizing a curated database of past high-performing content.
* **Task 2: Auto-Research Input Workflow (3 Pts):** Automated content engine processing live RSS data streams across high-signal technical feeds (Hacker News / TechCrunch AI) and scraping full text content via BeautifulSoup.
* **Task 3: Output Creation (Mandatory + 1 Pt Image Bonus):** Enforced structured Pydantic JSON responses parsing both finalized text variations and image conceptual layouts.
* **Task 4: Additional Features (2 Pts Bonus):** Custom architectural enhancements built out ahead of schedule:
  1. *Streamlit Monitoring Dashboard:* Interactive operational control center.
  2. *SQLite/SQLAlchemy Database Integration:* Isolated project storage engine (`nb_media_content.db`) keeping historical outputs persistent.

## Architecture Map
- `backend/main.py`: FastAPI Web App and API endpoint routes.
- `backend/agents/researcher.py`: Automated RSS and web scraping engine.
- `backend/agents/generator.py`: Advanced OpenAI system constraint mapper.
- `backend/agents/scheduler.py`: Pipeline executor operating via APScheduler.
- `backend/db/models.py`: Structured SQLAlchemy database layout.
- `frontend/app.py`: High-fidelity Streamlit user interface dashboard.

## Setup & Running Instructions
1. Initialize virtual environment and install packages: `pip install -r backend/requirements.txt`
2. Export your secret: `export OPENAI_API_KEY="sk-..."`
3. Launch backend services: `python3 -m uvicorn backend.main:app --reload`
4. Launch dashboard UI (in separate terminal tab): `python3 -m streamlit run frontend/app.py`