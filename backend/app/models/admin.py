"""数据库模型 - 管理员表"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="管理员 ID")
    username = Column(String(100), unique=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
