"""Endpoints for barcode lookups."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/{code}")
async def lookup_barcode(code: str) -> dict:
    """Return product data for a barcode.

    Placeholder implementation that echoes the code.
    """
    return {"code": code, "name": "unknown"}
