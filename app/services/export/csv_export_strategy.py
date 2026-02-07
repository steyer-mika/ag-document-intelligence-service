import csv
import io
from fastapi.responses import StreamingResponse

from app.services.export.export_strategy import ExportStrategy

class CsvExportStrategy(ExportStrategy):
    def export(self, job_id: int, extraction_result):
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            "article_number", "article_number_confidence",
            "description", "description_confidence",
            "kvk", "kvk_confidence",
            "wgp", "wgp_confidence",
            "quantity", "quantity_confidence",
            "price", "price_confidence",
            "total", "total_confidence",
        ])

        for pos in extraction_result.positions:
            writer.writerow([
                pos.article_number_value, pos.article_number_confidence,
                pos.description_value, pos.description_confidence,
                pos.kvk_value, pos.kvk_confidence,
                pos.wgp_value, pos.wgp_confidence,
                pos.quantity_value, pos.quantity_confidence,
                pos.price_value, pos.price_confidence,
                pos.total_value, pos.total_confidence,
            ])

        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=job_{job_id}.csv"
            },
        )
