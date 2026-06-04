import os
import sys

# Add the backend directory to the Python path dynamically
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from agents.scheduler import start_scheduler, run_auto_content_pipeline

app = FastAPI(title="NB Media LinkedIn Content Agent Backend")

@app.on_event("startup")
async def startup_event():
    """Runs automatically when the FastAPI server boots up."""
    start_scheduler()

@app.get("/")
def read_root():
    return {"status": "online", "agent": "Nikit Bassi Content System"}

@app.post("/api/v1/trigger-now")
async def trigger_pipeline_manually():
    """
    An endpoint your Streamlit frontend can hit to generate posts 
    on-demand without waiting for the morning cron schedule.
    """
    # Running this instantly to let you see your loop work on demand
    run_auto_content_pipeline()
    return {"status": "success", "message": "Pipeline execution triggered successfully."}