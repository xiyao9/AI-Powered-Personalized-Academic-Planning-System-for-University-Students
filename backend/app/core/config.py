"""应用核心配置"""
import os
from functools import lru_cache

class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/student_planning")
        self.ai_api_key = os.getenv("AI_API_KEY", "")
        self.ai_api_base = os.getenv("AI_API_BASE", "https://api.qwen.com/v1")
        self.ai_model = os.getenv("AI_MODEL", "qwen-max")

@lru_cache()
def get_settings():
    return Settings()
