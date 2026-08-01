import uuid
import datetime
from sqlalchemy import String, Integer, Numeric, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin

class Image(Base, TimestampMixin):
    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    listing: Mapped["Listing"] = relationship("Listing", back_populates="images")

    __table_args__ = (
        Index("ix_images_listing_order", "listing_id", "order"),
    )

class PriceHistory(Base):
    """
    Append-only log of price changes for tracking market dynamics over time.
    """
    __tablename__ = "price_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    marketplace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("marketplaces.id", ondelete="RESTRICT"), nullable=False)
    
    old_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    new_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    listing: Mapped["Listing"] = relationship("Listing", back_populates="price_history")
    marketplace: Mapped["Marketplace"] = relationship("Marketplace")
