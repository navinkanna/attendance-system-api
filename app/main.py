from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.database import Base, engine
from app.routers.class_router import router as class_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(class_router)


@app.get("/health")
def health():
    return {"status": "ok"}


handler = Mangum(app)
