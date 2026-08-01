import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin

class Marketplace(Base, TimestampMixin):
    """
    Supported marketplaces (e.g., OLX, Spinny, Cars24, Facebook).
    """
    __tablename__ = "marketplaces"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Relationships
    listings: Mapped[list["Listing"]] = relationship("Listing", back_populates="marketplace")
    sellers: Mapped[list["Seller"]] = relationship("Seller", back_populates="marketplace")
    scrape_jobs: Mapped[list["ScrapeJob"]] = relationship("ScrapeJob", back_populates="marketplace")
