import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import (
    UPLOAD_DIR,
    RESULTS_DIR,
    CORS_ORIGINS,
    API_TITLE,
    API_VERSION
)
from database import init_db
from routes import health, upload, scan, stats
from services.yolo_service import yolo_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan Context Manager.
    Initializes SQLite database and loads YOLOv8 model once at startup.
    """
    print("[Startup] Initializing Legal Metrology Package Compliance Scanner Backend...")
    print("[Startup] Initializing SQLite Scan History Database...")
    init_db()
    print(f"[Startup] Loading YOLOv8 Model (Status: {'Loaded' if yolo_service.is_loaded else 'Simulation Ready'})")
    yield
    print("[Shutdown] Cleaning up AI Scanner resources.")

# Initialize FastAPI Application
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=(
        "Production-ready FastAPI backend for Legal Metrology AI Package Label Compliance Scanner. "
        "Integrates YOLOv8 object detection, EasyOCR text extraction, OpenCV image processing, "
        "Legal Metrology rule compliance checking, and SQLite scan history analytics."
    ),
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Directories for Image Serving
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")

# Register API Routers
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(scan.router)
app.include_router(stats.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
