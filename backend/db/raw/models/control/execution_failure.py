from sqlalchemy import Column, Integer, String, DateTime, Text, func
from backend.db.raw.models.base import RawBase

class ExecutionFailure(RawBase):
    __tablename__ = "execution_failure"

    id = Column(Integer, primary_key=True)
    task_name = Column(String(200), nullable=False)
    engine_name = Column(String(100), nullable=True)
    entity_type = Column(String(100), nullable=True)
    entity_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    traceback = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
