from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PropertyModel(BaseModel):
    name: str = Field(max_length=100)
    address: str = Field(max_length=255)
    price: float = Field(gt=0)
    description: Optional[str] = None
    image_url: Optional[str] = None
    city: str = Field(max_length=100)
    is_available: bool = True
    zastroy_id: int


class PropertyResponse(PropertyModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PropertySearch(BaseModel):
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    is_available: Optional[bool] = True


class BookingModel(BaseModel):
    property_id: int


class BookingResponse(BaseModel):
    id: int
    user_id: int
    property_id: int
    booking_date: datetime
    status: str
    property: PropertyResponse

    class Config:
        from_attributes = True 