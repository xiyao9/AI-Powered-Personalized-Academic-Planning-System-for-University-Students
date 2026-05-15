"""数据库模型 - 打卡记录表"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date, JSON
from datetime import datetime
from .db import Base

class CheckInRecord(Base):
    __tablename__ = "checkin_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="打卡 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    check_in_date = Column(Date, nullable=False, comment="打卡日期")
    task_completed = Column(Text, comment="完成的任务")
    progress_notes = Column(Text, comment="进度备注")
    ai_feedback = Column(Text, comment="AI 反馈建议")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
