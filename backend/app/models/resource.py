"""数据库模型 - 学习资源表"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
import enum
from .db import Base

class ResourceType(str, enum.Enum):
    """资源类型枚举"""
    COURSE = "course"  # 网课
    BOOK = "book"  # 书籍
    WEBSITE = "website"  # 网站
    OTHER = "other"  # 其他

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="资源 ID")
    name = Column(String(200), nullable=False, comment="资源名称")
    resource_type = Column(Enum(ResourceType), nullable=False, comment="资源类型")
    target_major = Column(String(100), comment="适用专业")
    target_direction = Column(String(100), comment="适用方向")
    description = Column(Text, comment="资源描述")
    url = Column(String(500), comment="链接地址")
    quality_level = Column(String(50), comment="质量等级")
    is_recommended = Column(Integer, default=1, comment="是否推荐：1 是 0 否")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
