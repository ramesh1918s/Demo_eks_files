"""
routes/bookings.py — Booking API Endpoints
VayuBus Backend

POST /api/bookings              → create new booking
GET  /api/bookings/{pnr}        → get booking by PNR
GET  /api/bookings/phone/{phone}→ get bookings by phone
PUT  /api/bookings/{pnr}/cancel → cancel booking
GET  /api/admin/bookings        → all bookings (admin)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
import string
from datetime import datetime

from database import get_db
from models import Bus, BusRoute, Booking, Passenger
from schemas import BookingIn, BookingOut, BookingConfirmation

router = APIRouter(tags=["Bookings"])


# ── Generate unique PNR ────────────────────────
def generate_pnr(db: Session) -> str:
    while True:
        pnr = "VB" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exists = db.query(Booking).filter(Booking.pnr == pnr).first()
        if not exists:
            return pnr


# ── Price multiplier by passenger type ────────
def fare_multiplier(seat_type: str) -> float:
    return 0.6 if seat_type == "child" else 1.0


# ═══════════════════════════════════════════════
#  POST /api/bookings — Create Booking
# ═══════════════════════════════════════════════
@router.post("/api/bookings", response_model=BookingConfirmation, status_code=201)
def create_booking(payload: BookingIn, db: Session = Depends(get_db)):
    """
    Create a new booking with passenger details.
    Validates seat availability before confirming.
    """

    # ── Validate bus exists ────────────────────
    bus = db.query(Bus).filter(Bus.id == payload.bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # ── Check seats not already booked ────────
    existing_bookings = db.query(Booking).filter(
        Booking.bus_id      == payload.bus_id,
        Booking.journey_date == payload.journey_date,
        Booking.status       == "confirmed"
    ).all()

    already_booked = []
    for b in existing_bookings:
        already_booked.extend(b.seat_numbers)

    requested_seats = [p.seat_number for p in payload.passengers]
    conflicts = [s for s in requested_seats if s in already_booked]

    if conflicts:
        raise HTTPException(
            status_code=409,
            detail=f"Seats {conflicts} are already booked. Please select different seats."
        )

    # ── Calculate total amount ─────────────────
    total_amount = sum(
        bus.price * fare_multiplier(p.seat_type)
        for p in payload.passengers
    )

    # ── Create Booking ─────────────────────────
    pnr = generate_pnr(db)

    booking = Booking(
        pnr           = pnr,
        bus_id        = payload.bus_id,
        from_city     = payload.from_city,
        to_city       = payload.to_city,
        journey_date  = payload.journey_date,
        total_seats   = len(payload.passengers),
        seat_numbers  = requested_seats,
        total_amount  = round(total_amount, 2),
        status        = "confirmed",
        contact_phone = payload.contact_phone,
        contact_email = payload.contact_email
    )
    db.add(booking)
    db.flush()  # get booking.id

    # ── Create Passengers ──────────────────────
    passenger_outs = []
    for p in payload.passengers:
        fare = round(bus.price * fare_multiplier(p.seat_type), 2)
        passenger = Passenger(
            booking_id  = booking.id,
            seat_number = p.seat_number,
            seat_type   = p.seat_type,
            first_name  = p.first_name,
            last_name   = p.last_name,
            age         = p.age,
            id_proof    = p.id_proof,
            fare        = fare
        )
        db.add(passenger)
        passenger_outs.append({
            "seat_number": p.seat_number,
            "seat_type":   p.seat_type,
            "first_name":  p.first_name,
            "last_name":   p.last_name,
            "age":         p.age,
            "id_proof":    p.id_proof,
            "fare":        fare
        })

    db.commit()

    # ── Get route departure time ───────────────
    route = db.query(BusRoute).filter(
        BusRoute.bus_id    == payload.bus_id,
        BusRoute.from_city.ilike(f"%{payload.from_city}%"),
        BusRoute.to_city.ilike(f"%{payload.to_city}%")
    ).first()
    departure = route.departure if route else "—"

    return BookingConfirmation(
        pnr          = pnr,
        status       = "confirmed",
        from_city    = payload.from_city,
        to_city      = payload.to_city,
        journey_date = payload.journey_date,
        bus_name     = bus.name,
        departure    = departure,
        seats        = requested_seats,
        total_amount = round(total_amount, 2),
        passengers   = passenger_outs,
        message      = f"Booking confirmed! Your PNR is {pnr}. Have a safe journey! 🚌"
    )


# ═══════════════════════════════════════════════
#  GET /api/bookings/{pnr}
# ═══════════════════════════════════════════════
@router.get("/api/bookings/{pnr}", response_model=BookingOut)
def get_booking(pnr: str, db: Session = Depends(get_db)):
    """Get booking details by PNR"""
    booking = db.query(Booking).filter(Booking.pnr == pnr.upper()).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {pnr} not found")
    return booking


# ═══════════════════════════════════════════════
#  GET /api/bookings/phone/{phone}
# ═══════════════════════════════════════════════
@router.get("/api/bookings/phone/{phone}")
def get_bookings_by_phone(phone: str, db: Session = Depends(get_db)):
    """Get all bookings for a phone number"""
    bookings = db.query(Booking).filter(
        Booking.contact_phone == phone
    ).order_by(Booking.created_at.desc()).all()

    return {
        "phone":    phone,
        "count":    len(bookings),
        "bookings": [
            {
                "pnr":          b.pnr,
                "from_city":    b.from_city,
                "to_city":      b.to_city,
                "journey_date": b.journey_date,
                "seats":        b.seat_numbers,
                "amount":       b.total_amount,
                "status":       b.status,
                "booked_on":    b.created_at.strftime("%d %b %Y %H:%M")
            }
            for b in bookings
        ]
    }


# ═══════════════════════════════════════════════
#  PUT /api/bookings/{pnr}/cancel
# ═══════════════════════════════════════════════
@router.put("/api/bookings/{pnr}/cancel")
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    """Cancel a booking by PNR"""
    booking = db.query(Booking).filter(Booking.pnr == pnr.upper()).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {pnr} not found")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    booking.status = "cancelled"
    db.commit()

    return {
        "success": True,
        "pnr":     pnr,
        "message": f"Booking {pnr} cancelled successfully. Refund will be processed in 5-7 days."
    }


# ═══════════════════════════════════════════════
#  GET /api/admin/bookings — Admin
# ═══════════════════════════════════════════════
@router.get("/api/admin/bookings")
def get_all_bookings(
    skip:   int = 0,
    limit:  int = 50,
    db: Session = Depends(get_db)
):
    """Admin: Get all bookings with passenger details"""
    bookings = db.query(Booking)\
        .order_by(Booking.created_at.desc())\
        .offset(skip).limit(limit).all()

    total = db.query(Booking).count()
    confirmed = db.query(Booking).filter(Booking.status == "confirmed").count()
    cancelled = db.query(Booking).filter(Booking.status == "cancelled").count()
    revenue = db.query(Booking).filter(Booking.status == "confirmed").all()
    total_revenue = sum(b.total_amount for b in revenue)

    return {
        "stats": {
            "total":         total,
            "confirmed":     confirmed,
            "cancelled":     cancelled,
            "total_revenue": round(total_revenue, 2)
        },
        "bookings": [
            {
                "pnr":          b.pnr,
                "from_city":    b.from_city,
                "to_city":      b.to_city,
                "journey_date": b.journey_date,
                "seats":        b.seat_numbers,
                "passengers":   len(b.passengers),
                "amount":       b.total_amount,
                "status":       b.status,
                "phone":        b.contact_phone,
                "email":        b.contact_email,
                "booked_on":    b.created_at.strftime("%d %b %Y %H:%M")
            }
            for b in bookings
        ]
    }
