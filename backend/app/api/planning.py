"""API - 规划管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import User, PlanningScheme, get_db
from ..services.ai_service import AIService
from ..core.config import get_settings
from ..schemas.common import PlanningRequest, PlanningResponse

router = APIRouter()

@router.post("/generate", response_model=PlanningResponse)
async def generate_planning(request: PlanningRequest, db: Session = Depends(get_db)):
    """
    AI 生成专属规划
    """
    # 获取用户信息
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 检查是否已有规划
    existing_planning = db.query(PlanningScheme).filter(
        PlanningScheme.user_id == request.user_id
    ).first()

    if existing_planning and not request.generate_new:
        return existing_planning

    # 调用 AI 生成规划
    settings = get_settings()
    ai_service = AIService(
        api_key=settings.ai_api_key,
        api_base=settings.ai_api_base,
        model=settings.ai_model
    )

    user_info = {
        "name": user.name,
        "grade": user.grade,
        "major": user.major,
        "future_direction": user.future_direction,
        "weaknesses": user.weaknesses,
        "interests": user.interests
    }

    planning_content = ai_service.generate_planning(user_info)

    # 保存到数据库
    new_planning = PlanningScheme(
        user_id=user.id,
        year_plan="包含大一到大四的总体规划",
        semester_1_plan=planning_content,  # AI 生成的完整内容
        exam_list="见详细规划内容",
        internship_advice="详见实习建议部分",
        learning_tasks="请按照规划内容执行",
        time_schedule="请参考时间安排建议",
        ai_prompt_used=str(user_info),
        generated_at=datetime.now()
    )

    # 如果有旧规划，先删除
    if existing_planning:
        db.delete(existing_planning)

    db.add(new_planning)
    db.commit()
    db.refresh(new_planning)
    return new_planning

@router.get("/{user_id}", response_model=PlanningResponse)
async def get_user_planning(user_id: int, db: Session = Depends(get_db)):
    """获取用户的规划"""
    planning = db.query(PlanningScheme).filter(
        PlanningScheme.user_id == user_id
    ).first()

    if not planning:
        raise HTTPException(status_code=404, detail="未找到规划，请先使用生成接口")

    return planning

@router.delete("/{planning_id}")
async def delete_planning(planning_id: int, db: Session = Depends(get_db)):
    """删除规划"""
    planning = db.query(PlanningScheme).filter(
        PlanningScheme.id == planning_id
    ).first()

    if not planning:
        raise HTTPException(status_code=404, detail="规划不存在")

    db.delete(planning)
    db.commit()
    return {"message": "规划删除成功"}
