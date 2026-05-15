"""数据库模型 - 规划方案表"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from datetime import datetime
from .db import Base

class PlanningScheme(Base):
    __tablename__ = "planning_schemes"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="规划 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    year_plan = Column(String(500), comment="学年计划概要")
    semester_1_plan = Column(Text, comment="第一学期计划")
    semester_2_plan = Column(Text, comment="第二学期计划")
    exam_list = Column(Text, comment="必考证清单")
    internship_advice = Column(Text, comment="实习建议")
    learning_tasks = Column(Text, comment="学习任务")
    time_schedule = Column(String(500), comment="时间安排")
    ai_prompt_used = Column(Text, comment="使用的 AI 提示词")
    generated_at = Column(DateTime, default=datetime.now, comment="生成时间")
