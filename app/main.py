from fastapi import FastAPI
from app.db.database import engine
from app.db.tables import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Railway Ticket System")