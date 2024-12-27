from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.operation.router import router as operation
from src.api.place.router import router as place
from src.api.printer.router import router as printer

app = FastAPI(title="Manufactory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Если хочешь ограничить домены, можно указать конкретные.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    operation,
    prefix="/operation_history",
    tags=["Операции"]
)

app.include_router(
    place,
    prefix="/place",
    tags=["Устройства"]
)

app.include_router(
    printer,
    prefix="/printer",
    tags=["Принтер"]
)
