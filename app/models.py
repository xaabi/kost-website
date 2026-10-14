from sqlalchemy import Column, Integer, String, Float, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class RoomStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    type_name = Column(String(50), nullable=False)
    price_per_month = Column(Float, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    description = Column(Text, nullable=True)
    facilities = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class SurveyBooking(Base):
    __tablename__ = "survey_bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    survey_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("Room")
