"""Endpoints for image analysis."""

from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/")
async def analyze_image(file: UploadFile = File(...)) -> dict:
    """Process an uploaded meal photo.

    Returns the filename as a placeholder.
    """
    return {"filename": file.filename}
