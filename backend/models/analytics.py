import uuid
import datetime
from sqlalchemy import String, Numeric, DateTime, Index, Date
from sqlalchemy.orm import Mapped, mapped_column
from backend.models.base import Base
from backend.database.mixins import TimestampMixin

class AnalyticsMetric(Base, TimestampMixin):
    """
    Pre-aggregated metrics to serve dashboard charts instantly without heavy COUNT() queries 
    on the 10M+ rows listings table.
    """
    __tablename__ = "analytics_metrics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    dimension_key: Mapped[str | None] = mapped_column(String(255), nullable=True) # e.g. 'marketplace_id' or 'region'
    dimension_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metric_value: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)

    __table_args__ = (
        Index("ix_analytics_name_date", "metric_name", "date"),
    )
