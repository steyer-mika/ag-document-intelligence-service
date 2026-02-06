from fastapi import APIRouter
from app.celery_app import celery_app
from app.config.settings import settings

from app.api.dto import HealthResponse, InfoResponse

router = APIRouter()

@router.get("/", response_model=InfoResponse)
async def root():

    # log setting redis url and database host
    print(f"Redis URL: {settings.REDIS_URL}")
    print(f"Database Host: {settings.POSTGRES_HOST}")

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

@router.post("/jobs")
def create_job():
    celery_app.send_task(
        "app.worker.process_document",
        args=["test-job-id"],
    )

    return {"job_id": "test-job-id"}