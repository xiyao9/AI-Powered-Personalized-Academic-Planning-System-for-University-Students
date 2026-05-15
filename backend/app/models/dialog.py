"""数据库模型 - AI 对话记录表"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from .db import Base

class AIDialog(Base):
    __tablename__ = "ai_dialogs"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="对话 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    user_question = Column(Text, nullable=False, comment="用户问题")
    ai_answer = Column(Text, comment="AI 回答")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
