"""FastAPI 主应用入口"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .models.db import get_db
from .core.config import get_settings

app = FastAPI(
    title="AI 大学生学业规划系统",
    description="为大学生提供个性化四年学业规划和资源推荐",
    version="1.0.0"
)

# CORS 配置
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from .api import user_api, planning_api, resource_api, checkin_api, ai_api, admin_api

app.include_router(user_api, prefix="/api/user", tags=["用户管理"])
app.include_router(planning_api, prefix="/api/planning", tags=["规划管理"])
app.include_router(resource_api, prefix="/api/resource", tags=["资源管理"])
app.include_router(checkin_api, prefix="/api/checkin", tags=["打卡管理"])
app.include_router(ai_api, prefix="/api/ai", tags=["AI 服务"])
app.include_router(admin_api, prefix="/api/admin", tags=["后台管理"])

@app.get("/api")
async def root():
    return {
        "message": "AI 大学生学业规划系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
