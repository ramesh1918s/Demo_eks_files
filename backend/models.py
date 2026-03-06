"""
models.py — Database Table Definitions (SQLAlchemy ORM)
VayuBus Backend

Tables:
  - cities       : All cities
  - buses        : Bus details
  - bus_routes   : Route + stops per bus
  - bookings     : Booking master record
  - passengers   : Passenger details per booking seat
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ═══════════════════════════════════════════════
#  City
# ═══════════════════════════════════════════════
class City(Base):
    __tablename__ = "cities"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(100), unique=True, nullable=False, index=True)
    state    = Column(String(100), nullable=False)
    code     = Column(String(10), unique=True, nullable=False)   # e.g. "HYD"
    is_major = Column(Boolean, default=False)
    lat      = Column(Float, nullable=True)
    lng      = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ═══════════════════════════════════════════════
#  Bus
# ═══════════════════════════════════════════════
class Bus(Base):
    __tablename__ = "buses"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(150), nullable=False)
    bus_number   = Column(String(50), unique=True, nullable=False)
    operator     = Column(String(150), nullable=False)   # e.g. "VayuBus Travels"
    bus_type     = Column(String(100), nullable=False)   # e.g. "AC Sleeper 2+1"
    total_seats  = Column(Integer, nullable=False)
    layout       = Column(String(10), default="2+1")     # "2+1" or "2+2"
    decks        = Column(Integer, default=1)            # 1 or 2
    price        = Column(Float, nullable=False)         # base price per seat
    amenities    = Column(JSON, default=list)            # ["WiFi","AC","USB"]
    rating       = Column(Float, default=4.0)
    is_active    = Column(Boolean, default=True)

    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    routes    = relationship("BusRoute", back_populates="bus")
    bookings  = relationship("Booking",  back_populates="bus")


# ═══════════════════════════════════════════════
#  Bus Route
# ═══════════════════════════════════════════════
class BusRoute(Base):
    __tablename__ = "bus_routes"

    id           = Column(Integer, primary_key=True, index=True)
    bus_id       = Column(Integer, ForeignKey("buses.id"), nullable=False)
    from_city    = Column(String(100), nullable=False, index=True)
    to_city      = Column(String(100), nullable=False, index=True)
    departure    = Column(String(10), nullable=False)    # "06:30"
    arrival      = Column(String(10), nullable=False)    # "14:30"
    duration     = Column(String(20), nullable=False)    # "8h 00m"
    distance_km  = Column(Integer, nullable=True)
    stops        = Column(JSON, default=list)            # ["Stop1","Stop2"]
    stop_times   = Column(JSON, default=list)            # ["06:30","09:00"]
    days_of_week = Column(JSON, default=list)            # ["Mon","Tue",...] or ["Daily"]
    is_active    = Column(Boolean, default=True)

    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    bus = relationship("Bus", back_populates="routes")


# ═══════════════════════════════════════════════
#  Booking
# ═══════════════════════════════════════════════
class Booking(Base):
    __tablename__ = "bookings"

    id             = Column(Integer, primary_key=True, index=True)
    pnr            = Column(String(20), unique=True, nullable=False, index=True)
    bus_id         = Column(Integer, ForeignKey("buses.id"), nullable=False)
    from_city      = Column(String(100), nullable=False)
    to_city        = Column(String(100), nullable=False)
    journey_date   = Column(String(20), nullable=False)   # "2026-03-15"
    total_seats    = Column(Integer, nullable=False)
    seat_numbers   = Column(JSON, nullable=False)          # [3, 7, 12]
    total_amount   = Column(Float, nullable=False)
    status         = Column(String(20), default="confirmed")  # confirmed/cancelled

    # Contact details
    contact_phone  = Column(String(20), nullable=False)
    contact_email  = Column(String(150), nullable=False)

    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    bus        = relationship("Bus", back_populates="bookings")
    passengers = relationship("Passenger", back_populates="booking",
                              cascade="all, delete-orphan")


# ═══════════════════════════════════════════════
#  Passenger
# ═══════════════════════════════════════════════
class Passenger(Base):
    __tablename__ = "passengers"

    id           = Column(Integer, primary_key=True, index=True)
    booking_id   = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_number  = Column(Integer, nullable=False)
    seat_type    = Column(String(10), nullable=False)    # "male"/"female"/"child"
    first_name   = Column(String(100), nullable=False)
    last_name    = Column(String(100), nullable=False)
    age          = Column(Integer, nullable=False)
    id_proof     = Column(String(50), nullable=False)   # "Aadhaar"/"PAN"/etc
    fare         = Column(Float, nullable=False)         # actual fare charged

    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    booking = relationship("Booking", back_populates="passengers")
