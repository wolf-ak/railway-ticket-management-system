from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.tables import Train, TrainClass
from app.schemas.train_schema import TrainCreate, TrainResponse

router = APIRouter()


@router.post("/trains", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
def create_train(payload: TrainCreate, db: Session = Depends(get_db)):
    existing = db.query(Train).filter(Train.train_number == payload.train_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Train number already exists")

    train = Train(
        train_number=payload.train_number,
        train_name=payload.train_name,
        source=payload.source,
        destination=payload.destination,
    )
    db.add(train)
    db.flush()

    for cls in payload.classes:
        db.add(
            TrainClass(
                train_id=train.id,
                class_type=cls.class_type.strip(),
                total_seats=cls.total_seats,
                available_seats=cls.available_seats,
            )
        )

    db.commit()
    db.refresh(train)
    return train


@router.get("/trains", response_model=list[TrainResponse])
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
                "available_seats": cls.available_seats,
            }
            for cls in train.classes
        ],
    }
