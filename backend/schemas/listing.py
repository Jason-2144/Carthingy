import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ImageResponse(BaseModel):
    id: uuid.UUID
    image_url: str
    order: int
    model_config = ConfigDict(from_attributes=True)

class PriceHistoryResponse(BaseModel):
    id: uuid.UUID
    old_price: float | None
    new_price: float
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class SellerResponse(BaseModel):
    id: uuid.UUID
    name: str
    seller_type: str
    number_of_listings: int
    model_config = ConfigDict(from_attributes=True)

class MarketplaceResponse(BaseModel):
    id: uuid.UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

class ListingResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    price: float
    negotiable: bool
    registration_year: int
    km_driven: int
    ownership: int
    fuel: str | None
    transmission: str | None
    colour: str | None
    insurance: str | None
    registration_state: str
    registration_city: str
    status: str
    latitude: float | None
    longitude: float | None
    url: str
    first_seen: datetime
    last_seen: datetime
    
    seller: SellerResponse | None = None
    marketplace: MarketplaceResponse
    images: list[ImageResponse] = []
    price_history: list[PriceHistoryResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedListingsResponse(BaseModel):
    total: int
    items: list[ListingResponse]
    page: int
    size: int
