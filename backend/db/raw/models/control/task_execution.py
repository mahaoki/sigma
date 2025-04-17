from sqlalchemy import Column, Integer, String, DateTime, func
from backend.db.raw.models.base import RawBase

class TaskExecution(RawBase):
    __tablename__ = "task_execution"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(100), nullable=False, index=True)
    task_name = Column(String(200), nullable=False)
    status = Column(String(30), nullable=False, default="pending")
    start_time = Column(DateTime, nullable=False, default=func.now())
    end_time = Column(DateTime, nullable=True)
    message = Column(String, nullable=True)
