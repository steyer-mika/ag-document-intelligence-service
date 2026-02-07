from datetime import datetime, timezone

from app.celery_app import celery_app
from app.database.sync_session import SessionLocal
from app.database.models.job import Job, JobStatus 
from app.database.models.extraction_result import ExtractionResult
from app.database.models.order_position import OrderPosition
from app.services.orc_service import OrderPositionExtractionService
from app.utils.amount_to_float import amount_to_float
from app.utils.quantity_to_float import quantity_to_float

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

        extraction_result = ExtractionResult(
            job_id=job.id,
            total_pages=result.total_pages,
        )

        db.add(extraction_result)
        db.flush()

        for pos in result.positions:
            order_position = OrderPosition(
                extraction_result_id=extraction_result.id,
                article_number_value=pos.article_number.value,
                article_number_confidence=pos.article_number.confidence,
                description_value=pos.description.value,
                description_confidence=pos.description.confidence,
                kvk_value=pos.kvk.value,
                kvk_confidence=pos.kvk.confidence,
                wgp_value=pos.wgp.value,
                wgp_confidence=pos.wgp.confidence,
                quantity_value=quantity_to_float(pos.quantity.value), # postprocess to handle OCR errors and convert to float
                quantity_confidence=pos.quantity.confidence,
                price_value=amount_to_float(pos.price.value), # postprocess to handle OCR errors and convert to float
                price_confidence=pos.price.confidence,
                total_value=amount_to_float(pos.total.value), # postprocess to handle OCR errors and convert to float
                total_confidence=pos.total.confidence,
            )
            db.add(order_position)

        job.status = JobStatus.completed
        job.completed_at = datetime.now(timezone.utc)
        db.commit()

        return True

    except Exception as e:
        job.status = JobStatus.failed
        job.error = str(e)
        db.commit()
        raise
    finally:
        db.close()
