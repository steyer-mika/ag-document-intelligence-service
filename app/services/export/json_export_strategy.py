from app.services.export.export_strategy import ExportStrategy

class JsonExportStrategy(ExportStrategy):
    def export(self, job_id: int, extraction_result):
        return {
            "job_id": job_id,
            "total_pages": extraction_result.total_pages,
            "positions": [
                {
                    "article_number": {
                        "value": pos.article_number_value,
                        "confidence": pos.article_number_confidence,
                    },
                    "description": {
                        "value": pos.description_value,
                        "confidence": pos.description_confidence,
                    },
                    "kvk": {
                        "value": pos.kvk_value,
                        "confidence": pos.kvk_confidence
                    },
                    "wgp": {
                        "value": pos.wgp_value,
                        "confidence": pos.wgp_confidence
                    }
                }
                for pos in extraction_result.positions
            ],
        }
