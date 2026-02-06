from app.celery_app import celery_app

@celery_app.task(bind=True)
def process_document(self, job_id: int):
    import time
    time.sleep(10)  # Simulate time-consuming processing
    return f"Document processing for job {job_id} completed."
