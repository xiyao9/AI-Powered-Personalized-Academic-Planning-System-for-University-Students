"""API - 资源管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import Resource, ResourceType, get_db
from ..services.ai_service import AIService
from ..core.config import get_settings
from ..schemas.common import ResourceRecommendation

router = APIRouter()

@router.get("/recommendations", response_model=List[ResourceRecommendation])
async def get_recommendations(major: str, direction: str, db: Session = Depends(get_db)):
    """获取智能推荐的资源列表"""
    # 从数据库查询已有的推荐资源
    db_resources = db.query(Resource).filter(
        (Resource.target_major == major) |
        (Resource.target_major.is_(None)),
        Resource.is_recommended == 1
    ).limit(10).all()

    result = []
    for res in db_resources:
        result.append(ResourceRecommendation(
            name=res.name,
            resource_type=res.resource_type.value,
            description=res.description,
            url=res.url,
            is_recommended=bool(res.is_recommended)
        ))

    return result

@router.get("/list", response_model=List[dict])
async def list_resources(db: Session = Depends(get_db)):
    """列出所有资源"""
    resources = db.query(Resource).all()
    return [{
        "id": r.id,
        "name": r.name,
        "resource_type": r.resource_type.value,
        "target_major": r.target_major,
        "target_direction": r.target_direction,
        "description": r.description,
        "url": r.url,
        "is_recommended": bool(r.is_recommended)
    } for r in resources]

@router.post("/add")
async def add_resource(resource_data: dict, db: Session = Depends(get_db)):
    """添加新资源"""
    resource_type = ResourceType(resource_data.get("resource_type", "other"))

    new_resource = Resource(
        name=resource_data["name"],
        resource_type=resource_type,
        target_major=resource_data.get("target_major"),
        target_direction=resource_data.get("target_direction"),
        description=resource_data.get("description", ""),
        url=resource_data.get("url"),
        quality_level=resource_data.get("quality_level"),
        is_recommended=resource_data.get("is_recommended", 1),
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return {"message": "资源添加成功", "data": new_resource}

@router.delete("/{resource_id}")
async def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """删除资源"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    db.delete(resource)
    db.commit()
    return {"message": "资源删除成功"}
