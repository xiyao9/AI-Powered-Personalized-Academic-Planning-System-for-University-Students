# AI 大学生学业规划系统 - 快速部署指南

## 📋 项目概述

本项目是一个面向大学生的 AI 个性化学业规划系统，核心功能包括：
- 用户信息录入（年级、专业、发展方向）
- AI 自动生成专属大学四年规划
- 智能网课 & 学习资源推荐
- 规划进度打卡与 AI 反馈
- AI 智能问答

技术栈：Vue 3 + FastAPI + SQLAlchemy + MySQL + Qwen AI（可选）

---

## 🚀 快速启动（3 步完成）

### 环境要求

- **Python 3.8+**
- **MySQL 8.0+**
- **pip**（随 Python 安装）

> AI API Key 是可选的，没有 API Key 时系统会使用内置的模拟数据，所有功能仍可正常使用。

---

### 第 1 步：创建 MySQL 数据库

打开命令行，登录 MySQL：

```bash
mysql -u root -p
```

执行以下 SQL：

```sql
CREATE DATABASE IF NOT EXISTS student_planning
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

> 默认数据库连接：用户名 `root`，密码 `root`，端口 `3306`
> 如果你的 MySQL 密码不同，需要在配置中修改（见第 2 步）

---

### 第 2 步：安装依赖 & 初始化数据库

打开命令行，进入后端目录：

```bash
cd "AI 大学生学业规划系统/backend"

# 安装 Python 依赖
pip install -r requirements.txt

# 初始化数据库（自动创建表和初始数据）
python init_db.py
```

**如果你的 MySQL 密码不是 `root`**，需要先设置环境变量：

```bash
# Windows CMD
set MYSQL_PASSWORD=你的密码

# Windows PowerShell
$env:MYSQL_PASSWORD="你的密码"

# 然后再执行
python init_db.py
```

预期输出：
```
开始初始化数据库...
数据库已存在：student_planning
表结构创建完成！
默认数据插入完成！
数据库初始化完成！🎉
```

---

### 第 3 步：启动服务

```bash
python run_server.py
```

看到以下输出即表示启动成功：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🌐 访问系统

打开浏览器访问：

| 地址 | 说明 |
|------|------|
| http://localhost:8000 | 系统主页（Vue 前端） |
| http://localhost:8000/docs | API 接口文档（Swagger UI） |

### 测试账号

- **管理员**：用户名 `admin`，密码 `admin123`

---

## ✅ 功能测试流程

启动后按以下步骤测试：

1. **首页** → 访问 http://localhost:8000，查看功能介绍
2. **注册** → 点击"用户注册"，填写姓名、年级、专业、方向
3. **生成规划** → 注册成功后自动跳转到规划页面，点击"生成我的规划"
4. **学习资源** → 点击"学习资源"，查看推荐的网课和资料
5. **打卡** → 点击"打卡记录"，填写今日任务并提交
6. **AI 问答** → 点击"AI 问答"，输入问题（如"如何准备考研？"）
7. **后台管理** → 点击"后台管理"，用 admin/admin123 登录，管理模板和资源

> **没有 API Key 也能体验全部功能！** 系统内置了丰富的模拟数据，生成规划、资源推荐、AI 问答都会返回预设的高质量内容。

---

## 🔧 可选：配置真实 AI API

如果想使用真实的大模型 API（生成更个性化的内容）：

### 方式 1：环境变量

```bash
# Windows CMD
set AI_API_KEY=sk-你的key
set AI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
set AI_MODEL=qwen-max

# Windows PowerShell
$env:AI_API_KEY="sk-你的key"
$env:AI_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
$env:AI_MODEL="qwen-max"
```

### 方式 2：修改配置文件

编辑 `backend/app/core/config.py`，修改默认值：

```python
self.ai_api_key = os.getenv("AI_API_KEY", "sk-你的key")
self.ai_api_base = os.getenv("AI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
self.ai_model = os.getenv("AI_MODEL", "qwen-max")
```

> 兼容任何 OpenAI 格式的 API（通义千问、DeepSeek、智谱等），只需修改 `AI_API_BASE` 和 `AI_MODEL`。

---

## 🔧 常见问题

### Q1: `pip` 命令找不到

```bash
# Windows 使用 py -m pip
py -m pip install -r requirements.txt
```

### Q2: MySQL 连接失败

1. 确认 MySQL 服务已启动：`net start MySQL80`（Windows）
2. 确认用户名和密码正确
3. 确认端口为 3306

### Q3: 端口 8000 被占用

编辑 `run_server.py`，修改端口号：

```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # 改为 8001 或其他
```

### Q4: 前端页面空白 / 样式不显示

1. 确认 `run_server.py` 已正常启动（不是 `run.py`）
2. 检查浏览器控制台是否有 404 错误
3. 清除浏览器缓存后刷新

### Q5: 生成规划时响应较慢

- 使用模拟数据时响应很快（1 秒内）
- 使用真实 API 时，取决于网络和模型大小，可能需要 5-30 秒
- 请耐心等待，不要重复点击

---

## 📁 项目结构

```
AI 大学生学业规划系统/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口，注册所有路由
│   │   ├── api/
│   │   │   ├── __init__.py      # 路由导出
│   │   │   ├── user.py          # 用户注册/查询/删除
│   │   │   ├── planning.py      # 规划生成/查询/删除
│   │   │   ├── resource.py      # 资源推荐/管理
│   │   │   ├── checkin.py       # 打卡记录/统计
│   │   │   ├── ai.py            # AI 智能问答
│   │   │   └── admin.py         # 后台管理（模板/资源 CRUD）
│   │   ├── models/
│   │   │   ├── __init__.py      # 模型汇总
│   │   │   ├── db.py            # 数据库连接
│   │   │   ├── user.py          # 用户表
│   │   │   ├── planning.py      # 规划表
│   │   │   ├── resource.py      # 资源表
│   │   │   ├── checkin.py       # 打卡表
│   │   │   ├── dialog.py        # 对话表
│   │   │   ├── template.py      # 专业模板表
│   │   │   └── admin.py         # 管理员表
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── common.py        # Pydantic 数据模型
│   │   ├── services/
│   │   │   └── ai_service.py    # AI 服务（API 调用 + 模拟数据）
│   │   └── core/
│   │       └── config.py        # 全局配置
│   ├── requirements.txt         # Python 依赖
│   ├── init_db.py               # 数据库初始化脚本
│   ├── run.py                   # 开发模式启动（仅 API）
│   └── run_server.py            # 生产模式启动（API + 前端）
├── frontend/
│   ├── index.html               # Vue 3 单页应用
│   ├── css/main.css             # 样式文件
│   └── js/main.js               # 前端逻辑
├── DEPLOYMENT_GUIDE.md          # 部署指南
└── PROJECT_INTRODUCTION.md      # 项目介绍（适合申报/答辩）
```

---

## 📞 技术支持

如遇问题，请依次检查：
1. 终端是否有错误输出
2. MySQL 服务是否正常运行
3. 浏览器控制台（F12）Console 面板是否有报错
4. 访问 http://localhost:8000/health 确认后端可用

祝使用顺利！🎓
