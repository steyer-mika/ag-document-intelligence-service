from app.services.export.csv_export_strategy import CsvExportStrategy
from app.services.export.export_strategy import ExportStrategy
from app.services.export.json_export_strategy import JsonExportStrategy

class ExportFactory:
    _strategies = {
        "json": JsonExportStrategy(),
        "csv": CsvExportStrategy(),
    }

    @classmethod
    def get_strategy(cls, format: str) -> ExportStrategy:
        try:
            return cls._strategies[format]
        except KeyError:
            raise ValueError(f"Unsupported export format: {format}")
