"""数据库模型汇总"""
from .db import Base, engine, get_db, SQLALCHEMY_DATABASE_URL
from .user import User, FutureDirection, Grade
from .planning import PlanningScheme
from .resource import Resource, ResourceType
from .checkin import CheckInRecord
from .dialog import AIDialog
from .template import MajorTemplate
from .admin import Admin

# 创建所有表
def create_tables():
    Base.metadata.create_all(bind=engine)
