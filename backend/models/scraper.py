import uuid
import datetime
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin
from backend.models.enums import ScrapeJobStatus, LogLevel

class ScrapeJob(Base, TimestampMixin):
    __tablename__ = "scrape_jobs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    marketplace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("marketplaces.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[ScrapeJobStatus] = mapped_column(default=ScrapeJobStatus.PENDING, nullable=False, index=True)
    
    started_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metadata_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Store specific args

    marketplace: Mapped["Marketplace"] = relationship("Marketplace", back_populates="scrape_jobs")
    logs: Mapped[list["ScrapeLog"]] = relationship("ScrapeLog", back_populates="job", cascade="all, delete-orphan")


class ScrapeLog(Base, TimestampMixin):
    __tablename__ = "scrape_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("scrape_jobs.id", ondelete="CASCADE"), nullable=True, index=True)
    worker_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    log_level: Mapped[LogLevel] = mapped_column(default=LogLevel.INFO, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    job: Mapped["ScrapeJob"] = relationship("ScrapeJob", back_populates="logs")
