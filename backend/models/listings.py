import uuid
import datetime
from sqlalchemy import String, Integer, Numeric, Boolean, Text, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin, SoftDeleteMixin
from backend.models.enums import ListingStatus

class Listing(Base, TimestampMixin, SoftDeleteMixin):
    """
    Core listings table containing millions of rows. 
    Heavily indexed for high read-performance on search operations.
    """
    __tablename__ = "listings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    marketplace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("marketplaces.id", ondelete="RESTRICT"), nullable=False, index=True)
    car_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("cars.id", ondelete="RESTRICT"), nullable=True, index=True)
    seller_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("sellers.id", ondelete="SET NULL"), nullable=True, index=True)
    
    external_listing_id: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, index=True)
    negotiable: Mapped[bool] = mapped_column(Boolean, default=False)
    
    registration_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    km_driven: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    ownership: Mapped[int] = mapped_column(Integer, nullable=False) # e.g. 1st, 2nd owner
    
    # Redundant but useful fields for quick text search if car_id isn't matched yet
    fuel: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    colour: Mapped[str | None] = mapped_column(String(50), nullable=True)
    insurance: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    registration_state: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    registration_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    status: Mapped[ListingStatus] = mapped_column(default=ListingStatus.ACTIVE, nullable=False, index=True)
    
    # Geolocation for spatial querying
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    
    first_seen: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    # Relationships
    marketplace: Mapped["Marketplace"] = relationship("Marketplace", back_populates="listings")
    car: Mapped["Car"] = relationship("Car", back_populates="listings")
    seller: Mapped["Seller"] = relationship("Seller", back_populates="listings")
    images: Mapped[list["Image"]] = relationship("Image", back_populates="listing", cascade="all, delete-orphan", order_by="Image.order")
    price_history: Mapped[list["PriceHistory"]] = relationship("PriceHistory", back_populates="listing", cascade="all, delete-orphan", order_by="PriceHistory.timestamp.desc()")

    __table_args__ = (
        UniqueConstraint("marketplace_id", "external_listing_id", name="uq_marketplace_listing_ext_id"),
        Index("ix_listings_location", "registration_state", "registration_city"),
        Index("ix_listings_price_year_km", "price", "registration_year", "km_driven"), # Composite for common faceted search
    )
