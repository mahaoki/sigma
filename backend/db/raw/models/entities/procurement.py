from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from backend.db.raw.models.base import RawBase

class Procurement(RawBase):
    __tablename__ = "procurement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pncp_control_number = Column(String(50), unique=True, nullable=False, index=True)

    update_date = Column(DateTime, nullable=True, index=True)
    update_date_global = Column(DateTime, nullable=True, index=True)
    collected_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), index=True)

    raw_data = Column(JSONB, nullable=False)

    # Relationships (to be added later, e.g., items, contracts, documents, etc.)
