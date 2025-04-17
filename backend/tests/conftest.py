import pytest
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config.settings import settings
from backend.db.raw.models.base import RawBase
from backend.db.raw.models.control import * 

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(settings.RAW_TEST_DATABASE_URL)
    RawBase.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def period_id(db_session):
    period = ProcessingPeriod(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 1),
        status="test"
    )
    db_session.add(period)
    db_session.commit()
    return period.id