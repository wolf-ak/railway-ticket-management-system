from fastapi import FastAPI
from app.db.database import engine
from app.db.tables import Base
from app.routes import bookings, trains

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Railway Ticket System")

app.include_router(trains.router, tags=["Trains"])
app.include_router(bookings.router, tags=["Bookings"])


@app.get("/")
def root():
    return {"message": "Smart Railway Ticket System API is running"}
