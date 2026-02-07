from datetime import datetime, timezone
from app.celery_app import celery_app
from app.database.sync_session import SessionLocal
from app.database.models.job import Job, JobStatus 

from app.services.orc_service import OrderPositionExtractionService

@celery_app.task(bind=True)
def process_document(self, job_id: int):
    db = SessionLocal()

    try:
        job = db.query(Job).get(job_id)
        job.status = JobStatus.running
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        file_path = f"/files/{job.id}.pdf"

        orc_service = OrderPositionExtractionService()
        result = orc_service.extract_from_pdf(file_path)

        # Debug Dump to JSON to string to store in DB
        json_string = result.model_dump_json()

        job.status = JobStatus.completed
        job.completed_at = datetime.now(timezone.utc)
        job.result = json_string
        db.commit()

        return True

    except Exception as e:
        job.status = JobStatus.failed
        job.result = str(e)
        db.commit()
        raise
    finally:
        db.close()
