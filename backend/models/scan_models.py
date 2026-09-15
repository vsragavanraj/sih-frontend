from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DashboardStatsResponse(BaseModel):
    """
    Response schema for GET /stats endpoint
    Example:
    {
       "total_scans": 100,
       "compliant": 82,
       "non_compliant": 18,
       "accuracy": 96
    }
    """
    total_scans: int = Field(..., example=100)
    compliant: int = Field(..., example=82)
    non_compliant: int = Field(..., example=18)
    accuracy: int = Field(..., example=96)

class DetectionItem(BaseModel):
    """
    YOLOv8 detected package label field schema.
    """
    class_name: str = Field(..., alias="class", example="MRP")
    confidence: float = Field(..., example=0.95)
    bbox: List[int] = Field(..., example=[120, 240, 320, 300])

    class Config:
        populate_by_name = True

class YoloDetectionResponse(BaseModel):
    """
    Response format for POST /detect endpoint
    """
    detections: List[DetectionItem]

class FieldExtractionResponse(BaseModel):
    """
    Response format for POST /extract-fields endpoint
    """
    extracted_fields: Dict[str, str] = Field(
        ...,
        example={
            "MRP": "₹120",
            "NET_QUANTITY": "500g"
        }
    )

class ComplianceEngineRequest(BaseModel):
    """
    Request model for POST /validate-compliance endpoint
    """
    fields: Dict[str, str] = Field(
        ...,
        example={
            "MRP": "₹120",
            "Manufacturer Name": "PepsiCo India Ltd",
            "Net Quantity": "500g",
            "Manufacturing Date": "12/08/2025",
            "Expiry Date": "12/08/2027"
        }
    )

class ComplianceEngineResponse(BaseModel):
    """
    Response model for Legal Metrology Compliance Engine
    """
    status: str = Field(..., example="COMPLIANT")
    score: int = Field(..., example=96)
    missing_fields: List[str] = Field(default_factory=list, example=[])

class UploadResponse(BaseModel):
    """
    Response format for POST /upload endpoint
    """
    image_id: str = Field(..., example="123")
    status: str = Field("uploaded", example="uploaded")
    filename: Optional[str] = Field(None, example="package_label.jpg")

class HealthResponse(BaseModel):
    """
    Response format for GET /health endpoint
    """
    status: str = Field("healthy", example="healthy")
    service: str = Field("Package Label Compliance Scanner API", example="Package Label Compliance Scanner API")
    version: str = Field("1.0.0", example="1.0.0")
    yolo_model_loaded: bool = Field(True, example=True)
    ocr_engine_ready: bool = Field(True, example=True)
    timestamp: str = Field(..., example="2026-08-28T10:40:00Z")

class ChecklistItem(BaseModel):
    name: str = Field(..., example="MRP (Maximum Retail Price)")
    status: bool = Field(..., example=True)
    note: Optional[str] = Field(None, example="Declared inclusive of all taxes")

class ViolationDetail(BaseModel):
    title: str = Field(..., example="Missing Complete Manufacturer Address")
    desc: str = Field(..., example="Rule 6(1)(a) requires principal place of business with valid postal PIN code.")
    legal_section: Optional[str] = Field("Rule 6(1)(a)", example="Rule 6(1)(a)")
    severity: Optional[str] = Field("High", example="High")

class CertificateMetadata(BaseModel):
    certificate_id: str = Field(..., example="LM-CERT-2026-98421")
    product_name: str = Field(..., example="Lays Classic Salted Potato Chips 50g")
    verification_date: str = Field(..., example="28 August 2026")
    verification_hash: str = Field(..., example="8f92a10b4c8932e...")
    status: str = Field(..., example="VERIFIED COMPLIANT")

class ScanResponse(BaseModel):
    status: str = Field(..., example="COMPLIANT")
    score: int = Field(..., example=96)
    detected_fields: Dict[str, str] = Field(
        ...,
        example={
            "MRP": "₹120",
            "NET_QUANTITY": "500g"
        }
    )
    missing_fields: List[str] = Field(default_factory=list, example=[])

    scan_id: Optional[str] = Field(None, example="SC-98421")
    filename: Optional[str] = Field(None, example="package_label.jpg")
    file_url: Optional[str] = Field(None, example="/uploads/SC-98421_package_label.jpg")
    annotated_url: Optional[str] = Field(None, example="/results/SC-98421_annotated.jpg")
    product_name: Optional[str] = Field(None, example="Lays Potato Chips 50g")
    risk_level: Optional[str] = Field(None, example="Low Risk")
    fine_estimate: Optional[str] = Field(None, example="₹0 (Fully Compliant)")
    checklist: Optional[List[ChecklistItem]] = None
    violations: Optional[List[ViolationDetail]] = None
    recommendations: Optional[List[str]] = None
    detections: Optional[List[DetectionItem]] = None
    certificate: Optional[CertificateMetadata] = None
    processed_timestamp: Optional[str] = Field(None, example="2026-08-28T10:40:00Z")
