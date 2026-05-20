"""API Schema - 数据验证模型"""
from pydantic import BaseModel, field_serializer
from typing import Optional, Union
from datetime import datetime, date

# 用户相关 Schema
class UserCreate(BaseModel):
    name: str
    grade: str
    major: str
    future_direction: str
    weaknesses: Optional[str] = ""
    interests: Optional[str] = ""

class UserResponse(BaseModel):
    id: int
    name: str
    grade: str
    major: str
    future_direction: str
    weaknesses: Optional[str]
    interests: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# 规划相关 Schema
class PlanningRequest(BaseModel):
    user_id: int
    generate_new: bool = True

class PlanningResponse(BaseModel):
    id: int
    user_id: int
    year_plan: Optional[str]
    semester_1_plan: Optional[str]
    semester_2_plan: Optional[str]
    exam_list: Optional[str]
    internship_advice: Optional[str]
    learning_tasks: Optional[str]
    time_schedule: Optional[str]
    generated_at: datetime

    class Config:
        from_attributes = True

# 资源推荐 Schema
class ResourceRecommendation(BaseModel):
    name: str
    resource_type: str
    description: str
    url: Optional[str] = None
    is_recommended: bool = True

# 打卡记录 Schema
class CheckInCreate(BaseModel):
    user_id: int
    check_in_date: str
    task_completed: str
    progress_notes: Optional[str] = ""

class CheckInRecordResponse(BaseModel):
    id: int
    user_id: int
    check_in_date: str
    task_completed: str
    progress_notes: Optional[str]
    ai_feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d') if v else None
        }

# AI 问答 Schema
class QuestionRequest(BaseModel):
    user_id: int
    question: str
    context: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    user_id: int
    user_question: str
    ai_answer: str
    created_at: datetime

    class Config:
        from_attributes = True

# 通用响应格式
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
