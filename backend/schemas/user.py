from pydantic import BaseModel, ConfigDict
import uuid
import datetime

class UserBase(BaseModel):
    email: str
    role: str = "user"
    is_active: bool = True
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    model_config = ConfigDict(from_attributes=True)
