import enum
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Enum,
)
from sqlalchemy.sql import func
from app.database.base import Base


class JobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(
        Enum(JobStatus, name="job_status"),
        nullable=False,
        default=JobStatus.pending,
    )

    error = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
