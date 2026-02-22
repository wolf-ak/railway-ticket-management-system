from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.tables import Train, TrainClass
from app.models.train import TrainOut

router = APIRouter()

@router.get("/trains", response_model=list[TrainOut])
def get_trains(db: Session = Depends(get_db)):
    trains = db.query(Train).all()
    return trains

@router.get("/trains/{train_id}")
def get_train_details(train_id: int, db: Session = Depends(get_db)):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return {
        "train_number": train.train_number,
        "train_name": train.train_name,
        "source": train.source,
        "destination": train.destination,
        "classes": [
            {
                "class_type": cls.class_type,
                "total_seats": cls.total_seats,
                "available_seats": cls.available_seats
            }
            for cls in train.classes
        ]
    }