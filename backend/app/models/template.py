"""数据库模型 - 专业模板表"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .db import Base

class MajorTemplate(Base):
    __tablename__ = "major_templates"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="模板 ID")
    major_name = Column(String(100), nullable=False, comment="专业名称")
    core_courses = Column(Text, comment="核心课程")
    recommended_certificates = Column(Text, comment="推荐证书")
    career_path = Column(Text, comment="职业路径")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
