"""API - 打卡管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List

from ..models import User, CheckInRecord, get_db
from ..services.ai_service import AIService
from ..core.config import get_settings
from ..schemas.common import CheckInCreate, CheckInRecordResponse

router = APIRouter()

@router.post("/checkin")
async def create_checkin(record: CheckInCreate, db: Session = Depends(get_db)):
    """创建打卡记录"""
    # 检查用户是否存在
    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 解析日期
    check_date = datetime.strptime(record.check_in_date, "%Y-%m-%d").date()

    # 获取 AI 反馈
    settings = get_settings()
    ai_service = AIService(
        api_key=settings.ai_api_key,
        api_base=settings.ai_api_base,
        model=settings.ai_model
    )

    context = f"学生专业：{user.major}, 发展方向：{str(user.future_direction)}"
    ai_feedback = await ai_service.answer_question(
        f"用户今天完成了这些任务：{record.task_completed}。根据用户的规划，给予一些鼓励和建议。",
        context
    )

    new_record = CheckInRecord(
        user_id=record.user_id,
        check_in_date=check_date,
        task_completed=record.task_completed,
        progress_notes=record.progress_notes,
        ai_feedback=ai_feedback,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "id": new_record.id,
        "user_id": new_record.user_id,
        "check_in_date": new_record.check_in_date.strftime("%Y-%m-%d"),
        "task_completed": new_record.task_completed,
        "progress_notes": new_record.progress_notes,
        "ai_feedback": new_record.ai_feedback,
        "created_at": new_record.created_at
    }

@router.get("/{user_id}/records")
async def get_user_checkins(user_id: int, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    """获取用户的打卡记录"""
    query = db.query(CheckInRecord).filter(CheckInRecord.user_id == user_id)

    if start_date:
        query = query.filter(CheckInRecord.check_in_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    if end_date:
        query = query.filter(CheckInRecord.check_in_date <= datetime.strptime(end_date, "%Y-%m-%d").date())

    records = query.order_by(CheckInRecord.check_in_date.desc()).all()
    return [{
        "id": r.id,
        "user_id": r.user_id,
        "check_in_date": r.check_in_date.strftime("%Y-%m-%d") if r.check_in_date else "",
        "task_completed": r.task_completed,
        "progress_notes": r.progress_notes,
        "ai_feedback": r.ai_feedback,
        "created_at": r.created_at
    } for r in records]

@router.get("/{user_id}/statistics")
async def get_checkin_statistics(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    """获取打卡统计"""
    from datetime import timedelta

    start_date = date.today() - timedelta(days=days)
    records = db.query(CheckInRecord).filter(
        CheckInRecord.user_id == user_id,
        CheckInRecord.check_in_date >= start_date
    ).all()

    total_records = len(records)
    consecutive_days = calculate_consecutive_days(records)

    return {
        "total_days": total_records,
        "consecutive_days": consecutive_days,
        "last_checkin_date": records[0].check_in_date.strftime("%Y-%m-%d") if records else None,
        "recent_records": [{
            "date": r.check_in_date.strftime("%Y-%m-%d"),
            "task": r.task_completed[:50] + "..." if len(r.task_completed) > 50 else r.task_completed
        } for r in records[:10]]
    }

def calculate_consecutive_days(records: List[CheckInRecord]) -> int:
    """计算连续打卡天数"""
    if not records:
        return 0

    dates = sorted([r.check_in_date for r in records], reverse=True)
    consecutive = 1

    for i in range(len(dates) - 1):
        diff = (dates[i] - dates[i+1]).days
        if diff == 1:
            consecutive += 1
        else:
            break

    return consecutive

@router.delete("/{record_id}")
async def delete_checkin(record_id: int, db: Session = Depends(get_db)):
    """删除打卡记录"""
    record = db.query(CheckInRecord).filter(CheckInRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="打卡记录不存在")

    db.delete(record)
    db.commit()
    return {"message": "打卡记录删除成功"}
