from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    floor = Column(Integer)
    numbers = Column(Integer)

class Peer(Base):
    __tablename__ = 'peers'
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    nick = Column(String, unique=True, index=True)

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    peer_id = Column(Integer, ForeignKey('peers.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    room = relationship("Room")
    peer = relationship("Peer")
