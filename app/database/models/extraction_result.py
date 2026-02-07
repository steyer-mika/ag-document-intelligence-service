from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class ExtractionResult(Base):
    __tablename__ = "extraction_results"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, unique=True)

    total_pages = Column(Integer, nullable=False)

    job = relationship("Job", backref="extraction_result")
    positions = relationship(
        "OrderPosition",
        back_populates="result",
        cascade="all, delete-orphan",
    )
