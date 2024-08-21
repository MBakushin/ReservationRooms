from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, schemas
from .database import engine, SessionLocal, Base
from fastapi.middleware.cors import CORSMiddleware
from .admin import app as admin_app


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/admin", admin_app)
# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/rooms/", response_model=list[schemas.Room])
def read_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)

@app.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    room = crud.get_room(db, booking.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return crud.create_booking(db, booking.room_id, booking.peer_id, booking.start_time, booking.end_time)
