from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.database import Base, engine
from app.models import (  # noqa: F401 (register models for create_all)
    attendance_model,
    class_model,
    class_registration_model,
    student_model,
)
from app.routers.attendance_router import router as attendance_router
from app.routers.class_registration_router import router as class_registration_router
from app.routers.class_router import router as class_router
from app.routers.student_router import router as student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://attendance-system-ui.pages.dev"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(class_router)
app.include_router(student_router)
app.include_router(class_registration_router)
app.include_router(attendance_router)


@app.get("/health")
def health():
    return {"status": "ok"}


handler = Mangum(app)
