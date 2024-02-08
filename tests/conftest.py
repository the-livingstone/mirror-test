import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base_db import Base
from app.db.orm import WalkerORM
from app.deps import get_db
from app.main import get_app
from app.models import get_uid

DATABASE_URL = "sqlite://"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_override():
    try:
        db = session()
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    db = session()
    walkers = [
        WalkerORM(name="Пётр", uid=get_uid()),
        WalkerORM(name="Антон", uid=get_uid()),
    ]
    db.add_all(walkers)
    db.commit()


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    init_db()
    app = get_app()
    app.dependency_overrides[get_db] = get_db_override
    return TestClient(app)
