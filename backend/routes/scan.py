import os
import uuid
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Path as FastAPIPath

from config import UPLOAD_DIR, ALLOWED_EXTENSIONS
from services.yolo_service import yolo_service
from services.compliance_service import compliance_service
from services.compliance_engine import compliance_engine
from models.scan_models import (
    YoloDetectionResponse,
    ScanResponse,
    DetectionItem,
    FieldExtractionResponse,
    ComplianceEngineRequest,
    ComplianceEngineResponse
)

router = APIRouter(tags=["Package Scanner"])

@router.post("/scan", response_model=ScanResponse, status_code=status.HTTP_200_OK)
async def scan_package_image(file: UploadFile = File(...)):
    """
    POST /scan - Complete AI Pipeline Endpoint
    
    Workflow:
    Upload Image -> YOLO Detection -> OCR Extraction -> Compliance Validation -> Generate Report
    
    Response Example:
    {
       "status": "COMPLIANT",
       "score": 96,
       "detected_fields": {
          "MRP": "₹120",
          "NET_QUANTITY": "500g"
       },
       "missing_fields": []
    }
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{file_ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    unique_id = f"SC-{uuid.uuid4().hex[:6].upper()}"
    sanitized_filename = f"{unique_id}_{file.filename.replace(' ', '_')}"
    saved_file_path = UPLOAD_DIR / sanitized_filename

    try:
        contents = await file.read()
        with open(saved_file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Execute Complete AI Pipeline
    scan_report = compliance_service.process_image_scan(
        str(saved_file_path),
        file.filename
    )

    return ScanResponse(**scan_report)


@router.post("/validate-compliance", response_model=ComplianceEngineResponse, status_code=status.HTTP_200_OK)
async def validate_label_compliance(body: ComplianceEngineRequest):
    """
    POST /validate-compliance - Legal Metrology Compliance Engine Endpoint
    """
    if not body or not body.fields:
        raise HTTPException(status_code=400, detail="No fields provided for compliance evaluation.")

    result = compliance_engine.validate_fields(body.fields)
    return ComplianceEngineResponse(**result)


@router.post("/extract-fields", response_model=FieldExtractionResponse, status_code=status.HTTP_200_OK)
async def extract_fields_ocr(file: UploadFile = File(...)):
    """
    POST /extract-fields - EasyOCR after YOLO Detection Endpoint
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    temp_filename = f"ocr_{uuid.uuid4().hex[:6]}_{file.filename.replace(' ', '_')}"
    saved_path = UPLOAD_DIR / temp_filename

    try:
        contents = await file.read()
        with open(saved_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

    extracted_dict = compliance_service.ocr_after_yolo(str(saved_path))
    return FieldExtractionResponse(extracted_fields=extracted_dict)


@router.post("/detect", response_model=YoloDetectionResponse, status_code=status.HTTP_200_OK)
async def detect_label_fields(file: UploadFile = File(...)):
    """
    POST /detect - Custom YOLOv8 Label Field Detection API
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    temp_filename = f"detect_{uuid.uuid4().hex[:6]}_{file.filename.replace(' ', '_')}"
    saved_path = UPLOAD_DIR / temp_filename

    try:
        contents = await file.read()
        with open(saved_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

    result = yolo_service.detect_fields(str(saved_path))
    
    detection_models = [
        DetectionItem(
            class_name=d["class"],
            confidence=d["confidence"],
            bbox=d["bbox"]
        )
        for d in result.get("detections", [])
    ]

    return YoloDetectionResponse(detections=detection_models)


@router.post("/scan/{image_id}", response_model=ScanResponse, status_code=status.HTTP_200_OK)
async def scan_by_image_id(image_id: str = FastAPIPath(..., description="ID returned from POST /upload")):
    """
    POST /scan/{image_id} - Scan Pre-uploaded Package Image by Image ID
    """
    matching_files = list(UPLOAD_DIR.glob(f"{image_id}_*"))
    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail=f"Image with image_id '{image_id}' not found in uploads folder."
        )

    target_file = matching_files[0]
    scan_report = compliance_service.process_image_scan(
        str(target_file),
        target_file.name
    )

    return ScanResponse(**scan_report)
