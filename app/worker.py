from datetime import datetime, timezone
from app.celery_app import celery_app
from app.database.sync_session import SessionLocal
from app.database.models.job import Job, JobStatus 

@celery_app.task(bind=True)
def process_document(self, job_id: int):
    db = SessionLocal()

    try:
        job = db.query(Job).get(job_id)
        job.status = JobStatus.running
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        result = f"Processed document {job_id}"

        import time
        time.sleep(10)  # Simulate time-consuming processing

        job.status = JobStatus.completed
        job.completed_at = datetime.now(timezone.utc)
        job.result = result
        db.commit()

        return result

    except Exception as e:
        job.status = JobStatus.failed
        job.result = str(e)
        db.commit()
        raise
    finally:
        db.close()
