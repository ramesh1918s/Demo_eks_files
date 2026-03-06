"""
routes/cities.py — Cities API Endpoints
VayuBus Backend

GET /api/cities           → all cities
GET /api/cities/major     → major cities only
GET /api/cities/search    → search by name
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import City
from schemas import CityOut

router = APIRouter(prefix="/api/cities", tags=["Cities"])


@router.get("/", response_model=List[CityOut])
def get_all_cities(db: Session = Depends(get_db)):
    """Get all cities sorted by name"""
    return db.query(City).order_by(City.name).all()


@router.get("/major", response_model=List[CityOut])
def get_major_cities(db: Session = Depends(get_db)):
    """Get only major cities"""
    return db.query(City).filter(City.is_major == True).order_by(City.name).all()


@router.get("/search", response_model=List[CityOut])
def search_cities(
    q: str = Query(..., min_length=2, description="City name to search"),
    db: Session = Depends(get_db)
):
    """Search cities by name (partial match)"""
    return db.query(City).filter(
        City.name.ilike(f"%{q}%")
    ).order_by(City.name).limit(10).all()
