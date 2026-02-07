from abc import ABC, abstractmethod
from typing import Any

class ExportStrategy(ABC):
    @abstractmethod
    def export(self, job_id: int, extraction_result) -> Any:
        pass