"""静态文件服务和完整应用启动"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

app = FastAPI(
    title="AI 大学生学业规划系统",
    description="为大学生提供个性化四年学业规划和资源推荐",
    version="1.0.0"
)

frontend_path = Path(__file__).parent.parent / "frontend"

# 分别挂载 css 和 js 目录，匹配 HTML 中的引用路径
app.mount("/css", StaticFiles(directory=str(frontend_path / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(frontend_path / "js")), name="js")

# 导入并挂载 API 路由
from app.main import app as api_app

for route in api_app.routes:
    app.router.routes.append(route)

@app.get("/")
async def serve_frontend():
    return FileResponse(frontend_path / "index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
