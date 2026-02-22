from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String(20), unique=True, nullable=False)
    train_name = Column(String(100), nullable=False)
    source = Column(String(100))
    destination = Column(String(100))

    classes = relationship("TrainClass", back_populates="train")


class TrainClass(Base):
    __tablename__ = "train_classes"

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    class_type = Column(String(20))  # Sleeper, 3AC, 2AC
    total_seats = Column(Integer)
    available_seats = Column(Integer)

    train = relationship("Train", back_populates="classes")