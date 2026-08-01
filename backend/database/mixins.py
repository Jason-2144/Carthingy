import datetime
from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column
from sqlalchemy.sql import func

@declarative_mixin
class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to a model."""
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

@declarative_mixin
class SoftDeleteMixin:
    """Mixin for soft-delete functionality."""
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
