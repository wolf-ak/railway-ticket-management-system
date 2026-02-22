from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.database import get_db
from app.db.tables import Booking, TrainClass
from app.schemas.booking_schema import BookingCreate, BookingResponse

router = APIRouter()


def generate_pnr():
    return str(uuid.uuid4())[:8].upper()


@router.post("/book", response_model=BookingResponse)
def book_ticket(payload: BookingCreate, db: Session = Depends(get_db)):
    class_type = payload.class_type.strip()
    train_class = (
        db.query(TrainClass)
        .filter(
            TrainClass.train_id == payload.train_id,
            TrainClass.class_type == class_type,
        )
        .with_for_update()
        .first()
    )

    if not train_class:
        raise HTTPException(
            status_code=404,
            detail=(
                "Train class not found for given train_id and class_type"
            ),
        )

    if train_class.available_seats > 0:
        train_class.available_seats -= 1
        booking = Booking(
            pnr=generate_pnr(),
            user_name=payload.user_name,
            train_id=train_class.train_id,
            class_type=train_class.class_type,
            seat_number=train_class.total_seats - train_class.available_seats,
            status="CONFIRMED",
            waiting_position=None,
        )
    else:
        waiting_count = (
            db.query(Booking)
            .filter(
                Booking.train_id == train_class.train_id,
                Booking.class_type == train_class.class_type,
                Booking.status == "WAITING",
            )
            .count()
        )
        booking = Booking(
            pnr=generate_pnr(),
            user_name=payload.user_name,
            train_id=train_class.train_id,
            class_type=train_class.class_type,
            seat_number=None,
            status="WAITING",
            waiting_position=waiting_count + 1,
        )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.post("/cancel/{pnr}")
def cancel_ticket(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = "CANCELLED"

    if booking.seat_number:
        train_class = (
            db.query(TrainClass)
            .filter(
                TrainClass.train_id == booking.train_id,
                TrainClass.class_type == booking.class_type,
            )
            .with_for_update()
            .first()
        )
        if train_class:
            train_class.available_seats += 1

            waiting = (
                db.query(Booking)
                .filter(
                    Booking.train_id == booking.train_id,
                    Booking.class_type == booking.class_type,
                    Booking.status == "WAITING",
                )
                .order_by(Booking.waiting_position.asc())
                .first()
            )

            if waiting:
                waiting.status = "CONFIRMED"
                waiting.seat_number = (
                    train_class.total_seats - train_class.available_seats + 1
                )
                waiting.waiting_position = None
                train_class.available_seats -= 1

    db.commit()
    return {"message": "Ticket cancelled successfully"}


@router.get("/bookings/{user_name}", response_model=list[BookingResponse])
def get_user_bookings(user_name: str, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.user_name == user_name).all()
    return bookings
