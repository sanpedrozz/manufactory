from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.alarm.src.routers.router import router as alarms

app = FastAPI(title="Manufactory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    alarms,
    prefix="/alarms",
    tags=["Аварии"]
)
