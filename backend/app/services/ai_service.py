"""AI 服务 - 调用大模型 API"""
from typing import Optional
import os
import json
import asyncio

class AIService:
    """AI 服务类，封装大模型 API 调用"""

    def __init__(self, api_key: str, api_base: str, model: str):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

    async def generate_planning(self, user_info: dict) -> str:
        """根据用户信息生成专属规划（异步）"""
        prompt = f"""你是一位资深的大学生学业规划师。请为以下学生制定一份详细的大学四年规划：

【学生基本信息】
- 姓名：{user_info.get('name', '未知')}
- 年级：{self._get_chinese_grade(user_info.get('grade'))}
- 专业：{user_info.get('major', '未知')}
- 未来方向：{self._get_direction_desc(user_info.get('future_direction'))}
- 自身短板：{user_info.get('weaknesses', '无特别说明')}
- 兴趣倾向：{user_info.get('interests', '无特别说明')}

【要求】
1. 按学年分解规划（大一到大四）
2. 每个学期要有明确的学习重点
3. 列出必须考取的证书清单
4. 给出实习建议和时间安排
5. 结合用户的专业和发展方向，给出个性化建议

请以清晰的 Markdown 格式输出，包含：
- 学年规划总览
- 分学期详细计划
- 考证清单
- 实习建议
- 时间管理建议"""

        response = await self._call_api(prompt)
        return response

    async def get_resource_recommendations(self, major: str, direction: str) -> list:
        """获取学习资源推荐（异步）"""
        prompt = f"""请为{major}专业、发展方向为{self._get_direction_desc(direction)}的学生推荐学习资源。

要求推荐：
1. 高质量网课平台及具体课程
2. 经典参考书籍
3. 实用网站和工具
4. 刷题练习资源

每条资源包括：名称、类型、简要说明、推荐理由。
用 JSON 格式返回，不要其他多余内容。"""

        response = await self._call_api(prompt)
        try:
            if "```json" in response:
                response = response.replace("```json", "").replace("```", "")
            return json.loads(response.strip())
        except:
            return [{"name": "通用资源", "type": "course", "description": response}]

    async def answer_question(self, question: str, context: Optional[str] = None) -> str:
        """回答学生问题（异步）"""
        system_prompt = "你是一位经验丰富的大学学业规划顾问，擅长为学生提供专业发展、考研、就业、考公等方面的指导。"
        user_prompt = f"""我的问题是：{question}

{'背景信息：' + context if context else ''}

请给出专业、实用、可操作的建议。"""

        response = await self._call_api(system_prompt + "\n\n" + user_prompt, is_chat=True)
        return response

    async def _call_api(self, prompt: str, is_chat: bool = False) -> str:
        """异步调用 API 的通用方法，使用 aiohttp 避免阻塞事件循环"""
        try:
            import aiohttp
            url = f"{self.api_base}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是一个专业的助手"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API 调用失败：{e}")
            return self._get_mock_response(prompt)

    def _get_mock_response(self, prompt: str) -> str:
        """模拟响应（当 API 不可用时，提供更丰富的演示数据）"""
        if "生成规划" in prompt or "四年规划" in prompt or "学业规划师" in prompt:
            return """# 大学生四年学业规划方案

## 一、学年规划总览

### 大一：适应探索期
- **学习目标**：打好专业基础，适应大学学习方式，了解专业前景
- **关键任务**：通过英语四级，打好数学和编程基础（如适用）
- **实践活动**：加入 1-2 个社团，探索兴趣方向
- **自我提升**：培养自主学习能力，学会利用图书馆和网络资源

### 大二：能力提升期
- **学习目标**：深入学习专业核心课程，提升综合能力
- **关键任务**：通过英语六级，考取计算机二级等基础证书
- **实践活动**：参加学科竞赛（如互联网+、挑战杯），争取奖学金
- **自我提升**：开始关注考研或就业信息，确定大致方向

### 大三：定向深化期
- **学习目标**：确定发展方向，深度准备目标所需能力
- **关键任务**：
  - 考研方向：开始系统复习，确定目标院校
  - 就业方向：积累项目经验，准备简历和面试
  - 考公方向：了解考试大纲，开始行测申论复习
- **实践活动**：寻找对口实习机会，积累实战经验

### 大四：冲刺收获期
- **学习目标**：完成毕业设计，实现升学或就业目标
- **关键任务**：考研冲刺复习 / 求职面试 / 公务员考试
- **实践活动**：毕业实习，顺利过渡到下一阶段

## 二、必考证清单

### 通用证书（所有专业建议）
1. **英语四级/六级** - 基本门槛，尽早通过
2. **计算机二级** - 办公技能证明
3. **普通话水平测试** - 教师/公务员必备

### 专业证书（根据专业有所差异）
- 计算机类：软考中级/高级、华为/阿里认证
- 经管类：证券从业、基金从业、初级会计
- 法学类：法律职业资格证书
- 师范类：教师资格证

### 技能加分项
- 驾驶证（建议大二前考取）
- 雅思/托福（留学或外企方向）

## 三、实习建议

- **大一暑假**：社会实践、志愿服务，积累社会经验
- **大二暑假**：尝试短期见习或项目实践，了解企业运作
- **大三暑假**：寻找对口岗位实习，积累专业经验（最关键）
- **大四上学期**：根据目标选择，考研党可适当减少实习

## 四、时间管理建议

1. **每日计划**：前一天晚上列好第二天要做的事
2. **番茄工作法**：25 分钟专注 + 5 分钟休息，提高效率
3. **周复盘**：每周日回顾本周完成情况，调整下周计划
4. **劳逸结合**：保证每天 7-8 小时睡眠，适当运动
5. **定期调整**：每学期末回顾规划执行情况，适时微调"""
        elif "推荐" in prompt and ("资源" in prompt or "网课" in prompt or "学习" in prompt):
            major = ""
            direction = ""
            if "专业" in prompt:
                import re
                m = re.search(r"为(.+?)专业", prompt)
                if m:
                    major = m.group(1)
            if "方向" in prompt:
                m = re.search(r"方向为(.+?)}", prompt)
                if m:
                    direction = m.group(1)

            return f"""# 推荐学习资源（{major or "通用"}专业 · {direction or "综合"}方向）

## 一、优质网课平台推荐

### 1. 中国大学 MOOC（icourse163.org）
- **特点**：国家级精品课程，免费学习，有证书
- **推荐**：搜索本专业核心课程，选 985/211 高校开设的

### 2. B站（bilibili.com）
- **特点**：免费、资源极多、社区活跃
- **推荐方法**：搜索"专业名 + 教程"或"专业名 + 考研"，按播放量排序

### 3. Coursera / edX
- **特点**：国际顶尖大学课程，有英文字幕
- **适合**：想提升英语和专业能力的同学

### 4. 网易云课堂 / 腾讯课堂
- **特点**：职业技能培训为主
- **适合**：就业方向的实用技能学习

## 二、经典书籍推荐

1. **《学会学习》** - 掌握高效学习方法
2. **《刻意练习》** - 技能提升的科学路径
3. **《深度工作》** - 培养专注力
4. **《被讨厌的勇气》** - 建立健康的自我认知

## 三、实用工具与网站

1. **学校图书馆数据库** - 免费获取学术资源
2. **知网（cnki.net）** - 中文文献检索
3. **GitHub** - 计算机专业必备
4. **Notion / 语雀** - 知识管理和笔记整理
5. **番茄ToDo** - 时间管理和打卡

## 四、刷题与练习资源

1. **LeetCode** - 编程能力训练
2. **牛客网** - 笔试面试真题
3. **粉笔公考** - 考公行测/申论刷题
4. **考研帮** - 考研真题和经验"""
        elif "打卡" in prompt or "任务" in prompt or "鼓励" in prompt or "建议" in prompt:
            return "太棒了！能看到你在坚持学习和打卡，这已经超过了大多数同学！\n\n**给你的几点建议：**\n\n1. **继续保持** - 坚持是最难的事，你在做一件很了不起的事\n2. **注意节奏** - 不要急于求成，按自己的节奏稳步前进\n3. **定期复盘** - 每周回顾一下哪些做得好、哪些可以改进\n4. **调整心态** - 偶尔没完成任务也没关系，重要的是第二天继续\n\n加油！每天进步一点点，四年后你会感谢现在努力的自己！"
        else:
            return f"""这是一个很好的问题！作为你的学业规划顾问，我来给你一些建议：

**关于你的问题，我的回答是：**

每个人的情况不同，但以下几点是通用的建议：

1. **明确目标** - 先想清楚自己想要什么，是考研、就业还是考公？
2. **拆解任务** - 把大目标分解为每月、每周可执行的小任务
3. **利用资源** - 善用 MOOC、B站等免费学习平台
4. **多向请教** - 主动找学长学姐和老师交流经验
5. **保持行动** - 规划再好不如行动，先做起来再优化

如果你有更具体的问题，欢迎继续向我提问！"""

    def _get_chinese_grade(self, grade_code: str) -> str:
        """将年级代码转换为中文"""
        grade_map = {
            "year1": "大一",
            "year2": "大二",
            "year3": "大三",
            "year4": "大四"
        }
        return grade_map.get(grade_code, "未知")

    def _get_direction_desc(self, direction: str) -> str:
        """将方向代码转换为中文描述"""
        direction_map = {
            "postgraduate": "考研深造",
            "employment": "直接就业",
            "civil_service": "考公务员",
            "abroad": "出国留学",
            "unsure": "暂未确定"
        }
        return direction_map.get(direction, "未知")
