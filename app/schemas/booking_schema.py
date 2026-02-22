from pydantic import BaseModel
from typing import Optional


# -------- Booking Create --------

class BookingCreate(BaseModel):
    train_id: int
    class_type: str
    user_name: str


# -------- Booking Response --------

class BookingResponse(BaseModel):
    id: int
    pnr: str
    train_id: int
    class_type: str
    status: str
    seat_number: Optional[int] = None
    waiting_position: Optional[int] = None

    class Config:
        orm_mode = True