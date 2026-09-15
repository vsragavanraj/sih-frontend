import os
from pathlib import Path

# Base Backend Directory
BASE_DIR = Path(__file__).resolve().parent

# File Directories
UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# File Upload Constraints
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}
MAX_FILE_SIZE_MB = 15
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# YOLO Model Configuration
YOLO_MODEL_PATH = "yolov8n.pt"

# CORS Settings
CORS_ORIGINS = [
    "*",  # Allow all origins for frontend access
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
]

# API Metadata
API_TITLE = "Legal Metrology Package Label Compliance Scanner API"
API_VERSION = "1.0.0"
