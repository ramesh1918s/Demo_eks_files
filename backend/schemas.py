"""
schemas.py — Pydantic Schemas for Request & Response Validation
VayuBus Backend
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime


# ═══════════════════════════════════════════════
#  City Schemas
# ═══════════════════════════════════════════════
class CityOut(BaseModel):
    id:       int
    name:     str
    state:    str
    code:     str
    is_major: bool
    lat:      Optional[float]
    lng:      Optional[float]

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════
#  Bus Schemas
# ═══════════════════════════════════════════════
class BusOut(BaseModel):
    id:          int
    name:        str
    bus_number:  str
    operator:    str
    bus_type:    str
    total_seats: int
    layout:      str
    decks:       int
    price:       float
    amenities:   List[str]
    rating:      float

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════
#  Bus Search Result Schema
# ═══════════════════════════════════════════════
class BusSearchResult(BaseModel):
    bus_id:       int
    bus_name:     str
    bus_number:   str
    operator:     str
    bus_type:     str
    layout:       str
    decks:        int
    departure:    str
    arrival:      str
    duration:     str
    distance_km:  Optional[int]
    price:        float
    amenities:    List[str]
    rating:       float
    total_seats:  int
    booked_seats: List[int]
    available:    int
    stops:        List[str]
    stop_times:   List[str]

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════
#  Passenger Schemas
# ═══════════════════════════════════════════════
class PassengerIn(BaseModel):
    seat_number: int
    seat_type:   str      # male / female / child
    first_name:  str
    last_name:   str
    age:         int
    id_proof:    str

    @field_validator("seat_type")
    @classmethod
    def validate_seat_type(cls, v):
        if v not in ["male", "female", "child"]:
            raise ValueError("seat_type must be male, female, or child")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v


class PassengerOut(BaseModel):
    seat_number: int
    seat_type:   str
    first_name:  str
    last_name:   str
    age:         int
    id_proof:    str
    fare:        float

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════
#  Booking Schemas
# ═══════════════════════════════════════════════
class BookingIn(BaseModel):
    bus_id:        int
    from_city:     str
    to_city:       str
    journey_date:  str
    contact_phone: str
    contact_email: str
    passengers:    List[PassengerIn]

    @field_validator("passengers")
    @classmethod
    def validate_passengers(cls, v):
        if len(v) < 1 or len(v) > 5:
            raise ValueError("Must have 1 to 5 passengers")
        seat_nums = [p.seat_number for p in v]
        if len(seat_nums) != len(set(seat_nums)):
            raise ValueError("Duplicate seat numbers not allowed")
        return v


class BookingOut(BaseModel):
    id:            int
    pnr:           str
    bus_id:        int
    from_city:     str
    to_city:       str
    journey_date:  str
    total_seats:   int
    seat_numbers:  List[int]
    total_amount:  float
    status:        str
    contact_phone: str
    contact_email: str
    passengers:    List[PassengerOut]
    created_at:    datetime

    class Config:
        from_attributes = True


class BookingConfirmation(BaseModel):
    pnr:          str
    status:       str
    from_city:    str
    to_city:      str
    journey_date: str
    bus_name:     str
    departure:    str
    seats:        List[int]
    total_amount: float
    passengers:   List[PassengerOut]
    message:      str


# ═══════════════════════════════════════════════
#  Generic Response
# ═══════════════════════════════════════════════
class APIResponse(BaseModel):
    success: bool
    message: str
    data:    Optional[dict] = None
