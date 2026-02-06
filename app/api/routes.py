from fastapi import APIRouter, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
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
async def health(db: AsyncSession = Depends(get_db)):
    is_database_connected = None

    try:
        # Check database connectivity
        await db.execute("SELECT 1")
        is_database_connected = True
    except Exception:
        is_database_connected = False

    return HealthResponse(
        status="ok" if is_database_connected else "unhealthy",
        service="Document Intelligence Service",
        is_database_connected="connected" if is_database_connected else "disconnected"
    )

@router.post("/jobs")
async def create_job(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # Validate file is PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
        
    # Create a new job in the database
    job = Job()
    db.add(job)

    # Commit the transaction to save the job and get its ID
    await db.commit()

    # Refresh the job instance to get the updated ID after commit
    await db.refresh(job)

    #! Note: In prd I would implement a more robust file storage solution like a blog storage
    #! For this example prototype I will skip the blob storage
    #! Just save the file to a local directory named "files" with the job ID as the filename
    file_path = f"/files/{job.id}.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Send a task to the Celery worker to process the document
    process_document.delay(job.id)

    return { "job_id": job.id }

@router.get("/jobs/{job_id}")
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await db.get(Job, job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job.id,
        "status": job.status.value,
        "result": job.result,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
    }