
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from services import get_status, add_water, reset_water, set_settings

app = FastAPI(title="Water Reminder Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DrinkPayload(BaseModel):
    amount: int

class SettingsPayload(BaseModel):
    reminder_interval_minutes: float | None = None
    stand_duration_minutes: float | None = None
    stand_enabled: bool | None = None

@app.get("/status")
async def status():
    return get_status()

@app.post("/drink")
async def drink(payload: DrinkPayload):
    try:
        return add_water(payload.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset")
async def reset():
    return reset_water()

@app.post("/settings")
async def settings(payload: SettingsPayload):
    return set_settings(
        reminder_interval=payload.reminder_interval_minutes,
        stand_duration=payload.stand_duration_minutes,
        stand_enabled=payload.stand_enabled
    )

# to run: uvicorn backend.app:app --reload --port 8000
