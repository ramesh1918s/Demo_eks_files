"""
routes/buses.py — Buses Search API Endpoints
VayuBus Backend

GET /api/buses                  → all buses
GET /api/buses/search           → search by from/to/date
GET /api/buses/{id}/booked      → booked seats for a bus on date
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Bus, BusRoute, Booking
from schemas import BusOut, BusSearchResult

router = APIRouter(prefix="/api/buses", tags=["Buses"])


@router.get("/", response_model=List[BusOut])
def get_all_buses(db: Session = Depends(get_db)):
    """Get all active buses"""
    return db.query(Bus).filter(Bus.is_active == True).all()


@router.get("/search", response_model=List[BusSearchResult])
def search_buses(
    from_city:     str = Query(..., description="Origin city"),
    to_city:       str = Query(..., description="Destination city"),
    journey_date:  str = Query(..., description="Journey date YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """
    Search buses by route and date.
    Returns buses with available seats and booked seat numbers.
    """
    # Find routes matching from/to
    routes = db.query(BusRoute).filter(
        BusRoute.from_city.ilike(f"%{from_city}%"),
        BusRoute.to_city.ilike(f"%{to_city}%"),
        BusRoute.is_active == True
    ).all()

    if not routes:
        return []

    results = []
    for route in routes:
        bus = route.bus

        # Get booked seats for this bus on this date
        bookings = db.query(Booking).filter(
            Booking.bus_id == bus.id,
            Booking.journey_date == journey_date,
            Booking.status == "confirmed"
        ).all()

        booked_seats = []
        for booking in bookings:
            booked_seats.extend(booking.seat_numbers)

        available = bus.total_seats - len(booked_seats)

        results.append(BusSearchResult(
            bus_id       = bus.id,
            bus_name     = bus.name,
            bus_number   = bus.bus_number,
            operator     = bus.operator,
            bus_type     = bus.bus_type,
            layout       = bus.layout,
            decks        = bus.decks,
            departure    = route.departure,
            arrival      = route.arrival,
            duration     = route.duration,
            distance_km  = route.distance_km,
            price        = bus.price,
            amenities    = bus.amenities or [],
            rating       = bus.rating,
            total_seats  = bus.total_seats,
            booked_seats = booked_seats,
            available    = available,
            stops        = route.stops or [],
            stop_times   = route.stop_times or []
        ))

    # Sort by price
    results.sort(key=lambda x: x.price)
    return results


@router.get("/{bus_id}/booked")
def get_booked_seats(
    bus_id:       int,
    journey_date: str = Query(..., description="Date YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Get list of booked seat numbers for a bus on a date"""
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    bookings = db.query(Booking).filter(
        Booking.bus_id == bus_id,
        Booking.journey_date == journey_date,
        Booking.status == "confirmed"
    ).all()

    booked = []
    for b in bookings:
        booked.extend(b.seat_numbers)

    return {
        "bus_id":       bus_id,
        "journey_date": journey_date,
        "booked_seats": booked,
        "total_seats":  bus.total_seats,
        "available":    bus.total_seats - len(booked)
    }
