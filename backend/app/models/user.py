"""数据库模型 - 用户信息表"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
import enum
from .db import Base

class FutureDirection(str, enum.Enum):
    """未来方向枚举"""
    POSTGRADUATE = "postgraduate"  # 考研
    EMPLOYMENT = "employment"  # 就业
    CIVIL_SERVICE = "civil_service"  # 考公
    ABROAD = "abroad"  # 留学
    UNSURE = "unsure"  # 暂未确定

class Grade(str, enum.Enum):
    """年级枚举"""
    YEAR1 = "year1"  # 大一
    YEAR2 = "year2"  # 大二
    YEAR3 = "year3"  # 大三
    YEAR4 = "year4"  # 大四

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户 ID")
    name = Column(String(100), nullable=False, comment="姓名")
    grade = Column(Enum(Grade, values_callable=lambda x: [e.value for e in x]), nullable=False, comment="年级")
    major = Column(String(100), nullable=False, comment="专业")
    future_direction = Column(Enum(FutureDirection, values_callable=lambda x: [e.value for e in x]), nullable=False, comment="未来方向")
    weaknesses = Column(Text, comment="自身短板")
    interests = Column(Text, comment="兴趣倾向")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
