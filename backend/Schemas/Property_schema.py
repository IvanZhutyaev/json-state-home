from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PropertyModel(BaseModel):
    name: str = Field(max_length=100)
    address: str = Field(max_length=255)
    price: int = Field(gt=0)
    description: Optional[str] = None
    image_url: Optional[str] = None
    city: str = Field(max_length=100)
    is_available: bool = True
    zastroy_id: int
    complex_id: Optional[int] = None
    area: Optional[int] = None  # Площадь в м²
    rooms: Optional[int] = None  # Количество комнат
    floor: Optional[int] = None  # Этаж


class PropertyResponse(PropertyModel):
    id: int
    area: Optional[int] = None
    rooms: Optional[int] = None
    floor: Optional[int] = None

    class Config:
        from_attributes = True


class PropertySearch(BaseModel):
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
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