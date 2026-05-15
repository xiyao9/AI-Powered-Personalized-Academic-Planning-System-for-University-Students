"""API - AI 智能问答"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import User, AIDialog, get_db
from ..services.ai_service import AIService
from ..core.config import get_settings
from ..schemas.common import QuestionRequest, QuestionResponse

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
async def ask_ai(question_req: QuestionRequest, db: Session = Depends(get_db)):
    """AI 智能问答接口"""
    # 验证用户
    user = db.query(User).filter(User.id == question_req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取 AI 回答
    settings = get_settings()
    ai_service = AIService(
        api_key=settings.ai_api_key,
        api_base=settings.ai_api_base,
        model=settings.ai_model
    )

    context = f"学生专业：{user.major}, 年级：{user.grade}, 发展方向：{user.future_direction}"
    ai_answer = ai_service.answer_question(question_req.question, context)

    # 保存对话记录
    new_dialog = AIDialog(
        user_id=user.id,
        user_question=question_req.question,
        ai_answer=ai_answer,
        created_at=datetime.now()
    )

    db.add(new_dialog)
    db.commit()
    db.refresh(new_dialog)
    return new_dialog

@router.get("/{user_id}/history", response_model=List[QuestionResponse])
async def get_dialog_history(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """获取用户的对话历史"""
    dialogs = db.query(AIDialog).filter(
        AIDialog.user_id == user_id
    ).order_by(AIDialog.created_at.desc()).limit(limit).all()
    return dialogs

@router.delete("/{dialog_id}")
async def delete_dialog(dialog_id: int, db: Session = Depends(get_db)):
    """删除对话记录"""
    dialog = db.query(AIDialog).filter(AIDialog.id == dialog_id).first()
    if not dialog:
        raise HTTPException(status_code=404, detail="对话记录不存在")

    db.delete(dialog)
    db.commit()
    return {"message": "对话记录删除成功"}
