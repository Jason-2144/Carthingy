import uuid
import datetime
from sqlalchemy import String, ForeignKey, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin
from backend.models.enums import TriggerType

class SavedListing(Base, TimestampMixin):
    __tablename__ = "saved_listings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="saved_listings")
    listing: Mapped["Listing"] = relationship("Listing")

    __table_args__ = (
        UniqueConstraint("user_id", "listing_id", name="uq_user_saved_listing"),
    )


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    query: Mapped[dict] = mapped_column(JSON, nullable=False) # JSON structure of the user's search query parameters
    trigger_type: Mapped[TriggerType] = mapped_column(nullable=False)
    last_triggered_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="alerts")
