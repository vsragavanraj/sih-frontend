import os
import uuid
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES
from models.scan_models import UploadResponse

router = APIRouter(tags=["Image Management"])

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_package_image(file: UploadFile = File(...)):
    """
    POST /upload - Package Image Upload Endpoint
    
    Accepts uploaded package label image, saves it to uploads/ folder,
    generates a unique image_id, and returns:
    {
       "image_id": "123",
       "status": "uploaded"
    }
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided or invalid filename."
        )

    # Validate File Extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read File Content & Check Size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum threshold of {MAX_FILE_SIZE_BYTES / (1024*1024)}MB."
        )

    # Generate Unique Image ID and Saved Filename
    image_id = str(uuid.uuid4().int)[:8]  # Clean numeric/alphanumeric ID (e.g. "12389412")
    sanitized_filename = f"{image_id}_{file.filename.replace(' ', '_')}"
    save_path = UPLOAD_DIR / sanitized_filename

    try:
        with open(save_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file to uploads storage: {str(e)}"
        )

    return UploadResponse(
        image_id=image_id,
        status="uploaded",
        filename=sanitized_filename
    )
