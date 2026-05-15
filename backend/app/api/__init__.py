"""API 路由汇总"""
from .user import router as user_api
from .planning import router as planning_api
from .resource import router as resource_api
from .checkin import router as checkin_api
from .ai import router as ai_api
from .admin import router as admin_api

__all__ = ["user_api", "planning_api", "resource_api", "checkin_api", "ai_api", "admin_api"]
