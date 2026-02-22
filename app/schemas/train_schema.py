from pydantic import BaseModel
from typing import List, Optional


# -------- TrainClass Schemas --------

class TrainClassBase(BaseModel):
    class_type: str
    total_seats: int
    available_seats: int


class TrainClassResponse(TrainClassBase):
    id: int

    class Config:
        orm_mode = True


# -------- Train Schemas --------

class TrainBase(BaseModel):
    train_number: str
    train_name: str
    source: str
    destination: str


class TrainCreate(TrainBase):
    classes: List[TrainClassBase]


class TrainResponse(TrainBase):
    id: int
    classes: List[TrainClassResponse] = []

    class Config:
        orm_mode = True