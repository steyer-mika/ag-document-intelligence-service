from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.dependencies import get_db
from app.database.models.job import Job
from app.config.settings import settings
from app.api.dto import HealthResponse, InfoResponse
from app.worker import process_document

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
async def create_job(db: Session = Depends(get_db)):
    # Create a new job in the database
    job = Job()
    db.add(job)

    # Commit the transaction to save the job and get its ID
    await db.commit()

    # Refresh the job instance to get the updated ID after commit
    await db.refresh(job)

    # Send a task to the Celery worker to process the document
    process_document.delay(job.id)

    return { "job_id": job.id }