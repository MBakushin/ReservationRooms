from sqlalchemy.orm import Session
from . import models

def get_rooms(db: Session):
    return db.query(models.Room).all()

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def create_booking(db: Session, room_id: int, peer_id: int, start_time: datetime, end_time: datetime):
    db_booking = models.Booking(room_id=room_id, peer_id=peer_id, start_time=start_time, end_time=end_time)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
