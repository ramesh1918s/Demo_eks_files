"""
seed_data.py — Seed Database with Cities, Buses & Routes
VayuBus Backend

Run: python seed_data.py
"""

from database import engine, SessionLocal
from models import Base, City, Bus, BusRoute

# ── Create all tables ─────────────────────────────────────────
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ═══════════════════════════════════════════════════════════════
#  CITIES — 50+ cities across India
# ═══════════════════════════════════════════════════════════════
CITIES = [
    # Telangana
    {"name": "Hyderabad",      "state": "Telangana",      "code": "HYD", "is_major": True,  "lat": 17.3850, "lng": 78.4867},
    {"name": "Warangal",       "state": "Telangana",      "code": "WGL", "is_major": False, "lat": 17.9784, "lng": 79.5941},
    {"name": "Nizamabad",      "state": "Telangana",      "code": "NZB", "is_major": False, "lat": 18.6725, "lng": 78.0941},
    {"name": "Khammam",        "state": "Telangana",      "code": "KHM", "is_major": False, "lat": 17.2473, "lng": 80.1514},
    # Andhra Pradesh
    {"name": "Vijayawada",     "state": "Andhra Pradesh", "code": "VJA", "is_major": True,  "lat": 16.5062, "lng": 80.6480},
    {"name": "Visakhapatnam",  "state": "Andhra Pradesh", "code": "VSK", "is_major": True,  "lat": 17.6868, "lng": 83.2185},
    {"name": "Tirupati",       "state": "Andhra Pradesh", "code": "TPT", "is_major": True,  "lat": 13.6288, "lng": 79.4192},
    {"name": "Guntur",         "state": "Andhra Pradesh", "code": "GNT", "is_major": False, "lat": 16.3067, "lng": 80.4365},
    {"name": "Kurnool",        "state": "Andhra Pradesh", "code": "KNL", "is_major": False, "lat": 15.8281, "lng": 78.0373},
    {"name": "Nellore",        "state": "Andhra Pradesh", "code": "NLR", "is_major": False, "lat": 14.4426, "lng": 79.9865},
    {"name": "Kakinada",       "state": "Andhra Pradesh", "code": "KKD", "is_major": False, "lat": 16.9891, "lng": 82.2475},
    # Tamil Nadu
    {"name": "Chennai",        "state": "Tamil Nadu",     "code": "CHN", "is_major": True,  "lat": 13.0827, "lng": 80.2707},
    {"name": "Coimbatore",     "state": "Tamil Nadu",     "code": "CBE", "is_major": True,  "lat": 11.0168, "lng": 76.9558},
    {"name": "Madurai",        "state": "Tamil Nadu",     "code": "MDU", "is_major": True,  "lat": 9.9252,  "lng": 78.1198},
    {"name": "Salem",          "state": "Tamil Nadu",     "code": "SLM", "is_major": False, "lat": 11.6643, "lng": 78.1460},
    {"name": "Trichy",         "state": "Tamil Nadu",     "code": "TRZ", "is_major": False, "lat": 10.7905, "lng": 78.7047},
    # Karnataka
    {"name": "Bengaluru",      "state": "Karnataka",      "code": "BLR", "is_major": True,  "lat": 12.9716, "lng": 77.5946},
    {"name": "Mysuru",         "state": "Karnataka",      "code": "MYS", "is_major": True,  "lat": 12.2958, "lng": 76.6394},
    {"name": "Mangaluru",      "state": "Karnataka",      "code": "MNG", "is_major": False, "lat": 12.9141, "lng": 74.8560},
    {"name": "Hubli",          "state": "Karnataka",      "code": "HBL", "is_major": False, "lat": 15.3647, "lng": 75.1240},
    {"name": "Belagavi",       "state": "Karnataka",      "code": "BGM", "is_major": False, "lat": 15.8497, "lng": 74.4977},
    # Maharashtra
    {"name": "Mumbai",         "state": "Maharashtra",    "code": "MUM", "is_major": True,  "lat": 19.0760, "lng": 72.8777},
    {"name": "Pune",           "state": "Maharashtra",    "code": "PNQ", "is_major": True,  "lat": 18.5204, "lng": 73.8567},
    {"name": "Nagpur",         "state": "Maharashtra",    "code": "NAG", "is_major": True,  "lat": 21.1458, "lng": 79.0882},
    {"name": "Nashik",         "state": "Maharashtra",    "code": "NSK", "is_major": False, "lat": 19.9975, "lng": 73.7898},
    {"name": "Aurangabad",     "state": "Maharashtra",    "code": "AWB", "is_major": False, "lat": 19.8762, "lng": 75.3433},
    {"name": "Solapur",        "state": "Maharashtra",    "code": "SUR", "is_major": False, "lat": 17.6805, "lng": 75.9064},
    # Delhi / NCR
    {"name": "Delhi",          "state": "Delhi",          "code": "DEL", "is_major": True,  "lat": 28.6139, "lng": 77.2090},
    {"name": "Gurgaon",        "state": "Haryana",        "code": "GGN", "is_major": False, "lat": 28.4595, "lng": 77.0266},
    {"name": "Noida",          "state": "Uttar Pradesh",  "code": "NOI", "is_major": False, "lat": 28.5355, "lng": 77.3910},
    # Rajasthan
    {"name": "Jaipur",         "state": "Rajasthan",      "code": "JAI", "is_major": True,  "lat": 26.9124, "lng": 75.7873},
    {"name": "Jodhpur",        "state": "Rajasthan",      "code": "JDH", "is_major": False, "lat": 26.2389, "lng": 73.0243},
    {"name": "Udaipur",        "state": "Rajasthan",      "code": "UDR", "is_major": False, "lat": 24.5854, "lng": 73.7125},
    # Gujarat
    {"name": "Ahmedabad",      "state": "Gujarat",        "code": "AMD", "is_major": True,  "lat": 23.0225, "lng": 72.5714},
    {"name": "Surat",          "state": "Gujarat",        "code": "STV", "is_major": True,  "lat": 21.1702, "lng": 72.8311},
    {"name": "Vadodara",       "state": "Gujarat",        "code": "BRC", "is_major": False, "lat": 22.3072, "lng": 73.1812},
    # UP & MP
    {"name": "Lucknow",        "state": "Uttar Pradesh",  "code": "LKO", "is_major": True,  "lat": 26.8467, "lng": 80.9462},
    {"name": "Agra",           "state": "Uttar Pradesh",  "code": "AGR", "is_major": True,  "lat": 27.1767, "lng": 78.0081},
    {"name": "Varanasi",       "state": "Uttar Pradesh",  "code": "VNS", "is_major": True,  "lat": 25.3176, "lng": 82.9739},
    {"name": "Bhopal",         "state": "Madhya Pradesh", "code": "BPL", "is_major": True,  "lat": 23.2599, "lng": 77.4126},
    {"name": "Indore",         "state": "Madhya Pradesh", "code": "IDR", "is_major": True,  "lat": 22.7196, "lng": 75.8577},
    # West Bengal
    {"name": "Kolkata",        "state": "West Bengal",    "code": "CCU", "is_major": True,  "lat": 22.5726, "lng": 88.3639},
    # Kerala
    {"name": "Kochi",          "state": "Kerala",         "code": "COK", "is_major": True,  "lat": 9.9312,  "lng": 76.2673},
    {"name": "Thiruvananthapuram","state":"Kerala",        "code": "TRV", "is_major": True,  "lat": 8.5241,  "lng": 76.9366},
    {"name": "Kozhikode",      "state": "Kerala",         "code": "CCJ", "is_major": False, "lat": 11.2588, "lng": 75.7804},
    # Punjab / Chandigarh
    {"name": "Chandigarh",     "state": "Chandigarh",     "code": "IXC", "is_major": True,  "lat": 30.7333, "lng": 76.7794},
    {"name": "Amritsar",       "state": "Punjab",         "code": "ATQ", "is_major": True,  "lat": 31.6340, "lng": 74.8723},
    {"name": "Ludhiana",       "state": "Punjab",         "code": "LUH", "is_major": False, "lat": 30.9010, "lng": 75.8573},
    # Others
    {"name": "Bhubaneswar",    "state": "Odisha",         "code": "BBI", "is_major": True,  "lat": 20.2961, "lng": 85.8245},
    {"name": "Raipur",         "state": "Chhattisgarh",   "code": "RPR", "is_major": True,  "lat": 21.2514, "lng": 81.6296},
    {"name": "Goa",            "state": "Goa",            "code": "GOI", "is_major": True,  "lat": 15.2993, "lng": 74.1240},
]

# ═══════════════════════════════════════════════════════════════
#  BUSES — 15 buses across different operators
# ═══════════════════════════════════════════════════════════════
BUSES = [
    {"name": "Shivneri Express",      "bus_number": "VB-001", "operator": "VayuBus Travels",   "bus_type": "AC Sleeper 2+1",      "total_seats": 36, "layout": "2+1", "decks": 2, "price": 650,  "amenities": ["WiFi","AC","USB","Blanket","Water","Pillow"], "rating": 4.5},
    {"name": "Volvo Gold Line",       "bus_number": "VB-002", "operator": "VayuBus Travels",   "bus_type": "AC Semi-Sleeper 2+2", "total_seats": 44, "layout": "2+2", "decks": 1, "price": 480,  "amenities": ["AC","Blanket","Water","USB"],                 "rating": 4.2},
    {"name": "Night Rider Deluxe",    "bus_number": "VB-003", "operator": "VayuBus Travels",   "bus_type": "Non-AC Sleeper 2+1",  "total_seats": 40, "layout": "2+1", "decks": 2, "price": 350,  "amenities": ["Pillow","Blanket","Water"],                   "rating": 3.9},
    {"name": "Deccan Queen",          "bus_number": "RR-001", "operator": "Royal Riders",      "bus_type": "AC Sleeper 2+1",      "total_seats": 36, "layout": "2+1", "decks": 2, "price": 720,  "amenities": ["WiFi","AC","USB","Blanket","Water","Snacks"],  "rating": 4.7},
    {"name": "Southern Star",         "bus_number": "RR-002", "operator": "Royal Riders",      "bus_type": "AC Seater 2+2",       "total_seats": 44, "layout": "2+2", "decks": 1, "price": 420,  "amenities": ["AC","Water","USB"],                           "rating": 4.1},
    {"name": "Mumbai Express",        "bus_number": "SM-001", "operator": "Speed Motors",      "bus_type": "AC Sleeper 2+1",      "total_seats": 36, "layout": "2+1", "decks": 2, "price": 850,  "amenities": ["WiFi","AC","USB","Blanket","Water","Pillow","Snacks"], "rating": 4.8},
    {"name": "Coastal Cruiser",       "bus_number": "SM-002", "operator": "Speed Motors",      "bus_type": "AC Semi-Sleeper 2+2", "total_seats": 44, "layout": "2+2", "decks": 1, "price": 550,  "amenities": ["AC","Water","USB","Charging"],                "rating": 4.3},
    {"name": "Metro Connect",         "bus_number": "CT-001", "operator": "City Transit",      "bus_type": "Non-AC Seater 2+2",   "total_seats": 52, "layout": "2+2", "decks": 1, "price": 280,  "amenities": ["Water"],                                     "rating": 3.7},
    {"name": "Rajdhani Sleeper",      "bus_number": "ND-001", "operator": "National Drives",   "bus_type": "AC Sleeper 2+1",      "total_seats": 36, "layout": "2+1", "decks": 2, "price": 950,  "amenities": ["WiFi","AC","USB","Blanket","Water","Pillow","Snacks","Entertainment"], "rating": 4.9},
    {"name": "Heritage Trails",       "bus_number": "ND-002", "operator": "National Drives",   "bus_type": "AC Semi-Sleeper 2+1", "total_seats": 40, "layout": "2+1", "decks": 1, "price": 600,  "amenities": ["AC","Water","USB","Blanket"],                 "rating": 4.4},
    {"name": "Greenline Volvo",       "bus_number": "GL-001", "operator": "Greenline Bus Co",  "bus_type": "AC Sleeper 2+1",      "total_seats": 36, "layout": "2+1", "decks": 2, "price": 780,  "amenities": ["WiFi","AC","USB","Blanket","Water"],           "rating": 4.6},
    {"name": "Patel Travels Premium", "bus_number": "PT-001", "operator": "Patel Travels",     "bus_type": "AC Sleeper 2+1",      "total_seats": 36, "layout": "2+1", "decks": 2, "price": 700,  "amenities": ["AC","USB","Blanket","Water","Pillow"],         "rating": 4.3},
    {"name": "KPN Gold",              "bus_number": "KP-001", "operator": "KPN Travels",       "bus_type": "AC Sleeper 2+1",      "total_seats": 40, "layout": "2+1", "decks": 2, "price": 680,  "amenities": ["AC","USB","Blanket","Water"],                 "rating": 4.2},
    {"name": "SRM Luxury",            "bus_number": "SR-001", "operator": "SRM Travels",       "bus_type": "AC Seater 2+2",       "total_seats": 44, "layout": "2+2", "decks": 1, "price": 450,  "amenities": ["AC","Water","USB"],                           "rating": 4.0},
    {"name": "Orange Tours",          "bus_number": "OT-001", "operator": "Orange Tours",      "bus_type": "Non-AC Sleeper 2+1",  "total_seats": 40, "layout": "2+1", "decks": 2, "price": 320,  "amenities": ["Water","Pillow"],                             "rating": 3.8},
]

# ═══════════════════════════════════════════════════════════════
#  ROUTES — Major routes with stops
# ═══════════════════════════════════════════════════════════════
ROUTES = [
    # Hyderabad routes
    {"bus_number": "VB-001", "from_city": "Hyderabad",    "to_city": "Chennai",       "departure": "21:00", "arrival": "06:00", "duration": "9h 00m",  "distance_km": 627,  "stops": ["Hyderabad (MGBS)","Nalgonda","Ongole","Nellore","Chennai (CMBT)"],          "stop_times": ["21:00","22:30","01:00","03:00","06:00"]},
    {"bus_number": "VB-002", "from_city": "Hyderabad",    "to_city": "Bengaluru",     "departure": "20:00", "arrival": "06:00", "duration": "10h 00m", "distance_km": 575,  "stops": ["Hyderabad (MGBS)","Kurnool","Anantapur","Bengaluru (Majestic)"],            "stop_times": ["20:00","22:00","01:00","06:00"]},
    {"bus_number": "VB-003", "from_city": "Hyderabad",    "to_city": "Vijayawada",    "departure": "06:00", "arrival": "11:00", "duration": "5h 00m",  "distance_km": 275,  "stops": ["Hyderabad (MGBS)","Suryapet","Miryalaguda","Vijayawada"],                   "stop_times": ["06:00","07:30","09:00","11:00"]},
    {"bus_number": "RR-001", "from_city": "Hyderabad",    "to_city": "Mumbai",        "departure": "17:00", "arrival": "09:00", "duration": "16h 00m", "distance_km": 711,  "stops": ["Hyderabad (MGBS)","Solapur","Pune","Mumbai (Dadar)"],                       "stop_times": ["17:00","22:00","04:00","09:00"]},
    {"bus_number": "RR-002", "from_city": "Hyderabad",    "to_city": "Tirupati",      "departure": "22:00", "arrival": "06:00", "duration": "8h 00m",  "distance_km": 520,  "stops": ["Hyderabad (MGBS)","Kurnool","Nellore","Tirupati"],                          "stop_times": ["22:00","01:00","04:00","06:00"]},
    # Bengaluru routes
    {"bus_number": "SM-001", "from_city": "Bengaluru",    "to_city": "Chennai",       "departure": "22:00", "arrival": "06:00", "duration": "8h 00m",  "distance_km": 346,  "stops": ["Bengaluru (Majestic)","Krishnagiri","Vellore","Chennai (CMBT)"],            "stop_times": ["22:00","00:30","03:00","06:00"]},
    {"bus_number": "SM-002", "from_city": "Bengaluru",    "to_city": "Goa",           "departure": "21:30", "arrival": "08:00", "duration": "10h 30m", "distance_km": 560,  "stops": ["Bengaluru (Majestic)","Hubli","Dharwad","Goa (Panaji)"],                    "stop_times": ["21:30","02:00","03:30","08:00"]},
    {"bus_number": "GL-001", "from_city": "Bengaluru",    "to_city": "Mysuru",        "departure": "07:00", "arrival": "10:00", "duration": "3h 00m",  "distance_km": 144,  "stops": ["Bengaluru (Majestic)","Mandya","Mysuru (Central)"],                         "stop_times": ["07:00","08:30","10:00"]},
    {"bus_number": "KP-001", "from_city": "Bengaluru",    "to_city": "Coimbatore",    "departure": "22:30", "arrival": "05:30", "duration": "7h 00m",  "distance_km": 365,  "stops": ["Bengaluru (Majestic)","Salem","Coimbatore (Gandhipuram)"],                  "stop_times": ["22:30","02:00","05:30"]},
    # Mumbai routes
    {"bus_number": "SM-001", "from_city": "Mumbai",       "to_city": "Pune",          "departure": "07:00", "arrival": "10:30", "duration": "3h 30m",  "distance_km": 148,  "stops": ["Mumbai (Dadar)","Khopoli","Pune (Swargate)"],                               "stop_times": ["07:00","09:00","10:30"]},
    {"bus_number": "ND-001", "from_city": "Mumbai",       "to_city": "Delhi",         "departure": "16:00", "arrival": "14:00", "duration": "22h 00m", "distance_km": 1421, "stops": ["Mumbai (Borivali)","Surat","Vadodara","Ahmedabad","Jaipur","Delhi (Kashmere Gate)"], "stop_times": ["16:00","20:00","22:30","02:00","09:00","14:00"]},
    {"bus_number": "PT-001", "from_city": "Mumbai",       "to_city": "Goa",           "departure": "22:00", "arrival": "08:00", "duration": "10h 00m", "distance_km": 594,  "stops": ["Mumbai (Dadar)","Ratnagiri","Goa (Panaji)"],                                "stop_times": ["22:00","03:00","08:00"]},
    # Chennai routes
    {"bus_number": "KP-001", "from_city": "Chennai",      "to_city": "Coimbatore",    "departure": "22:00", "arrival": "06:00", "duration": "8h 00m",  "distance_km": 497,  "stops": ["Chennai (CMBT)","Vellore","Salem","Coimbatore (Gandhipuram)"],              "stop_times": ["22:00","01:00","03:30","06:00"]},
    {"bus_number": "SR-001", "from_city": "Chennai",      "to_city": "Madurai",       "departure": "21:30", "arrival": "05:00", "duration": "7h 30m",  "distance_km": 462,  "stops": ["Chennai (CMBT)","Trichy","Dindigul","Madurai"],                             "stop_times": ["21:30","01:00","03:30","05:00"]},
    {"bus_number": "OT-001", "from_city": "Chennai",      "to_city": "Tirupati",      "departure": "06:00", "arrival": "10:00", "duration": "4h 00m",  "distance_km": 155,  "stops": ["Chennai (CMBT)","Nellore Bypass","Tirupati"],                               "stop_times": ["06:00","08:00","10:00"]},
    # Delhi routes
    {"bus_number": "ND-001", "from_city": "Delhi",        "to_city": "Jaipur",        "departure": "07:00", "arrival": "12:00", "duration": "5h 00m",  "distance_km": 281,  "stops": ["Delhi (Sarai Kale Khan)","Gurgaon","Dharuhera","Jaipur (SMS)"],             "stop_times": ["07:00","08:00","10:00","12:00"]},
    {"bus_number": "ND-002", "from_city": "Delhi",        "to_city": "Agra",          "departure": "06:00", "arrival": "10:00", "duration": "4h 00m",  "distance_km": 233,  "stops": ["Delhi (Kashmere Gate)","Faridabad","Mathura","Agra"],                       "stop_times": ["06:00","07:00","09:00","10:00"]},
    {"bus_number": "CT-001", "from_city": "Delhi",        "to_city": "Chandigarh",    "departure": "08:00", "arrival": "12:30", "duration": "4h 30m",  "distance_km": 261,  "stops": ["Delhi (Kashmere Gate)","Panipat","Ambala","Chandigarh"],                    "stop_times": ["08:00","09:30","11:00","12:30"]},
]


def seed():
    print("🌱 Seeding database...")

    # ── Cities ───────────────────────────────────
    existing_cities = db.query(City).count()
    if existing_cities == 0:
        for c in CITIES:
            db.add(City(**c))
        db.commit()
        print(f"  ✅ {len(CITIES)} cities added")
    else:
        print(f"  ⏭️  Cities already seeded ({existing_cities})")

    # ── Buses ────────────────────────────────────
    existing_buses = db.query(Bus).count()
    if existing_buses == 0:
        for b in BUSES:
            db.add(Bus(**b))
        db.commit()
        print(f"  ✅ {len(BUSES)} buses added")
    else:
        print(f"  ⏭️  Buses already seeded ({existing_buses})")

    # ── Routes ───────────────────────────────────
    existing_routes = db.query(BusRoute).count()
    if existing_routes == 0:
        for r in ROUTES:
            bus = db.query(Bus).filter(Bus.bus_number == r["bus_number"]).first()
            if bus:
                route_data = {k: v for k, v in r.items() if k != "bus_number"}
                route_data["bus_id"] = bus.id
                route_data["days_of_week"] = ["Daily"]
                db.add(BusRoute(**route_data))
        db.commit()
        print(f"  ✅ {len(ROUTES)} routes added")
    else:
        print(f"  ⏭️  Routes already seeded ({existing_routes})")

    print("🎉 Database seeding complete!")
    db.close()


if __name__ == "__main__":
    seed()
