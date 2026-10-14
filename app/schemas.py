from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoomBase(BaseModel):
    room_number: str
    title: str
    type_name: str
    price_per_month: float
    description: Optional[str] = None
    facilities: Optional[str] = None
    image_url: str

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    room_id: Optional[int] = None
    full_name: str
    phone_number: str
    survey_date: datetime
    notes: Optional[str] = None
