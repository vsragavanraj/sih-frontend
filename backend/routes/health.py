import datetime
from fastapi import APIRouter
from models.scan_models import HealthResponse
from services.yolo_service import yolo_service
from services.ocr_service import ocr_service

router = APIRouter(tags=["Health & Status"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    GET /health - API Health Check Endpoint
    Returns system status, YOLO model readiness, and timestamp.
    """
    return HealthResponse(
        status="healthy",
        service="Legal Metrology Package Label Compliance Scanner API",
        version="1.0.0",
        yolo_model_loaded=yolo_service.is_loaded,
        ocr_engine_ready=True,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
