"""
main.py — FastAPI Application Entry Point
VayuBus Backend

Start: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Docs:  http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from database import engine, Base
from models import City, Bus, BusRoute, Booking, Passenger   # noqa: F401 — needed for table creation
from routes import cities, buses, bookings

# ── Create all DB tables on startup ──────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI App ───────────────────────────────────────────────
app = FastAPI(
    title       = "VayuBus API",
    description = "Backend API for VayuBus Smart Bus Booking Platform",
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc"
)

# ── CORS — allow frontend to call API ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],   # In production: set your frontend URL
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Include Routers ───────────────────────────────────────────
app.include_router(cities.router)
app.include_router(buses.router)
app.include_router(bookings.router)


# ── Health Check ──────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "vayubus-backend"}


# ── Root ──────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "service":  "VayuBus API 🚌",
        "version":  "1.0.0",
        "docs":     "/docs",
        "redoc":    "/redoc",
        "endpoints": {
            "cities":   "/api/cities",
            "buses":    "/api/buses/search?from_city=Hyderabad&to_city=Chennai&journey_date=2026-03-15",
            "bookings": "/api/bookings",
            "admin":    "/api/admin/bookings"
        }
    }


# ── Startup event — seed data ─────────────────────────────────
@app.on_event("startup")
async def startup_event():
    from seed_data import seed
    try:
        seed()
        print("✅ VayuBus API started successfully!")
    except Exception as e:
        print(f"⚠️  Seed warning: {e}")
