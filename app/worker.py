from datetime import datetime, timezone

from app.celery_app import celery_app
from app.database.sync_session import SessionLocal
from app.database.models.job import Job, JobStatus 
from app.database.models.extraction_result import ExtractionResult
from app.database.models.order_position import OrderPosition
from app.services.orc_service import OrderPositionExtractionService
from app.utils.post_processing.article_number_post_processing import post_process_article_number
from app.utils.post_processing.description_post_processing import post_process_description
from app.utils.post_processing.kvk_post_processing import post_process_kvk
from app.utils.post_processing.wgp_post_processing import post_process_wgp

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
            article_number_value = post_process_article_number(pos.article_number.value)
            description_value = post_process_description(pos.description.value)
            kvk_value = post_process_kvk(pos.kvk.value)
            wgp_value = post_process_wgp(pos.wgp.value)

            order_position = OrderPosition(
                extraction_result_id=extraction_result.id,
                position_number=pos.position_number,
                article_number_value=article_number_value,
                article_number_confidence=pos.article_number.confidence if article_number_value else 0.0,
                description_value=description_value,
                description_confidence=pos.description.confidence if description_value else 0.0,
                kvk_value=kvk_value,
                kvk_confidence=pos.kvk.confidence if kvk_value else 0.0,
                wgp_value=wgp_value,
                wgp_confidence=pos.wgp.confidence if wgp_value else 0.0,
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
