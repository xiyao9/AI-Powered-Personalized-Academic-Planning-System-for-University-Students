"""API - 后台管理"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import Admin, User, MajorTemplate, Resource, get_db

router = APIRouter()
security = HTTPBearer()

# 简单密码验证（实际项目应该使用 JWT）
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # 建议修改

class AdminLoginRequest(BaseModel):
    username: str
    password: str

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """验证管理员身份"""
    username = credentials.credentials.split(":")[0] if ":" in credentials.credentials else ""
    password = credentials.credentials.split(":")[1] if ":" in credentials.credentials else ""

    # 简化验证（实际需要更好的认证机制）
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )

@router.post("/login")
async def admin_login(login_req: AdminLoginRequest):
    """管理员登录（返回简单的 token）"""
    if login_req.username == ADMIN_USERNAME and login_req.password == ADMIN_PASSWORD:
        # 生成简单 token（实际应使用 JWT）
        import base64
        import time
        token_data = f"{login_req.username}:{int(time.time())}"
        token = base64.b64encode(token_data.encode()).decode()
        return {"token": token, "expires_in": 86400}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """获取仪表盘数据"""
    user_count = db.query(User).count()
    planning_count = db.query(MajorTemplate).count()
    resource_count = db.query(Resource).count()

    return {
        "total_users": user_count,
        "total_planning": planning_count,
        "total_resources": resource_count,
        "recent_activity": "系统运行正常"
    }

@router.get("/templates/list", response_model=List[dict])
async def list_templates(db: Session = Depends(get_db)):
    """获取专业模板列表"""
    templates = db.query(MajorTemplate).all()
    return [{
        "id": t.id,
        "major_name": t.major_name,
        "core_courses": t.core_courses[:100] + "..." if t.core_courses else "",
        "created_at": t.created_at.strftime("%Y-%m-%d")
    } for t in templates]

@router.post("/templates/add")
async def add_template(template_data: dict, db: Session = Depends(get_db)):
    """添加专业模板"""
    new_template = MajorTemplate(
        major_name=template_data["major_name"],
        core_courses=template_data.get("core_courses", ""),
        recommended_certificates=template_data.get("recommended_certificates", ""),
        career_path=template_data.get("career_path", ""),
    )
    db.add(new_template)
    db.commit()
    return {"message": "模板添加成功"}

@router.delete("/templates/{template_id}")
async def delete_template(template_id: int, db: Session = Depends(get_db)):
    """删除模板"""
    template = db.query(MajorTemplate).filter(MajorTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    db.delete(template)
    db.commit()
    return {"message": "模板删除成功"}

@router.get("/resources/list", response_model=List[dict])
async def list_all_resources(db: Session = Depends(get_db)):
    """获取所有资源列表"""
    resources = db.query(Resource).all()
    return [{
        "id": r.id,
        "name": r.name,
        "resource_type": r.resource_type.value,
        "target_major": r.target_major,
        "target_direction": r.target_direction,
        "description": r.description[:100],
        "is_recommended": bool(r.is_recommended)
    } for r in resources]

@router.post("/resources/add")
async def add_resource(resource_data: dict, db: Session = Depends(get_db)):
    """添加资源"""
    from ..models import ResourceType
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
    return {"message": "资源添加成功"}

@router.delete("/resources/{resource_id}")
async def delete_admin_resource(resource_id: int, db: Session = Depends(get_db)):
    """删除资源"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")
    db.delete(resource)
    db.commit()
    return {"message": "资源删除成功"}
