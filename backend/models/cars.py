import uuid
from sqlalchemy import String, Integer, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
from backend.database.mixins import TimestampMixin

class Car(Base, TimestampMixin):
    """
    Represents a unique car model specification.
    Normalizing this prevents duplication of car metadata across 10M+ listings.
    """
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    variant: Mapped[str] = mapped_column(String(100), nullable=False)
    fuel: Mapped[str] = mapped_column(String(50), nullable=False)
    body_type: Mapped[str] = mapped_column(String(50), nullable=False)
    transmission: Mapped[str] = mapped_column(String(50), nullable=False)
    engine: Mapped[str] = mapped_column(String(100), nullable=True) # e.g. 1998cc
    seating: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationships
    listings: Mapped[list["Listing"]] = relationship("Listing", back_populates="car")

    __table_args__ = (
        UniqueConstraint("manufacturer", "make", "model", "variant", "fuel", "transmission", name="uq_car_spec"),
        Index("ix_cars_make_model", "make", "model"),
    )
