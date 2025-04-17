from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, UniqueConstraint, Index, func
from sqlalchemy.orm import relationship
from backend.db.raw.models.base import RawBase

class ProcurementCheck(RawBase):
    __tablename__ = "procurement_check"

    id = Column(Integer, primary_key=True, autoincrement=True)

    pncp_control_number = Column(String(50), nullable=False, index=True)
    action = Column(String(40), nullable=False)  # publication | update

    period_id = Column(Integer, ForeignKey("processing_period.id", ondelete="CASCADE"), nullable=True)
    period_date = Column(Date, nullable=True, index=True)

    status = Column(String(20), nullable=False, default="pending")  # pending | new | updated | ignored
    message = Column(String, nullable=True)

    executed_at = Column(DateTime, nullable=False, default=func.now())
    processed_at = Column(DateTime, nullable=True)

    update_date = Column(DateTime, nullable=True)
    update_date_global = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("pncp_control_number", "action", "period_date", name="uq_check_number_action_date"),
        Index("ix_check_status_period", "status", "period_date"),
    )

    period = relationship("ProcessingPeriod", backref="procurement_checks")
