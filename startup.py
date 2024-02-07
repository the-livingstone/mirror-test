from app.db.base_db import Base, engine, session
from app.db.orm import WalkerORM
from app.models import get_uid



def init_db():
    Base.metadata.create_all(bind=engine)

    db = session()

    walkers = [
        WalkerORM(name="Пётр", uid=get_uid()),
        WalkerORM(name="Антон", uid=get_uid())
    ]
    db.add_all(walkers)
    db.commit()

if __name__ == '__main__':
    init_db()