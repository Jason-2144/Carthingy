import uuid
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin
from backend.models.enums import SellerType

class Seller(Base, TimestampMixin):
    """
    Seller profile extracted from a marketplace.
    """
    __tablename__ = "sellers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    marketplace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("marketplaces.id", ondelete="CASCADE"), nullable=False, index=True)
    external_seller_id: Mapped[str] = mapped_column(String(255), nullable=True) # Marketplace specific ID if available
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_url: Mapped[str] = mapped_column(String(512), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    seller_type: Mapped[SellerType] = mapped_column(default=SellerType.INDIVIDUAL, nullable=False)
    number_of_listings: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    marketplace: Mapped["Marketplace"] = relationship("Marketplace", back_populates="sellers")
    listings: Mapped[list["Listing"]] = relationship("Listing", back_populates="seller")

    __table_args__ = (
        UniqueConstraint("marketplace_id", "external_seller_id", name="uq_seller_marketplace_ext_id"),
    )
