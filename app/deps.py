from app.db.base_db import session
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.repo import OrdersRepo
from app.service import OrderService

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def get_repo(db: Session = Depends(get_db)):
    return OrdersRepo(db)

def get_service(db: Session = Depends(get_db)):
    return OrderService(db)