from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    pnr = Column(String(20), unique=True, index=True)
    user_name = Column(String(100))
    train_id = Column(Integer, ForeignKey("trains.id"))
    class_type = Column(String(20))
    seat_number = Column(Integer, nullable=True)
    status = Column(String(20))  # CONFIRMED / WAITING / CANCELLED
    waiting_position = Column(Integer, nullable=True)

    train = relationship("Train")