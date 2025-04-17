from sqlalchemy import Column, Integer, String, Date, DateTime, func
from backend.db.raw.models.base import RawBase

class ProcessingPeriod(RawBase):
    __tablename__ = "processing_period"

    id = Column(Integer, primary_key=True, autoincrement=True)

    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)

    status = Column(String(20), nullable=False, default="pending")  # pending | running | processed | failed
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    reprocessed_at = Column(DateTime, nullable=True)

    total_checked_publications = Column(Integer, nullable=True)
    total_checked_updates = Column(Integer, nullable=True)
