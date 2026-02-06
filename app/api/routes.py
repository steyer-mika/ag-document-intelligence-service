from fastapi import APIRouter

from app.api.dto import HealthResponse, InfoResponse

router = APIRouter()

@router.get("/", response_model=InfoResponse)
async def root():
    return InfoResponse(
        app_name="Document Intelligence Service",
        version="1.0.0",
        description="Extracts structured data from documents using OCR technologies."
    )

@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service="Document Intelligence Service",
    )
