"""数据库初始化脚本"""
from sqlalchemy import create_engine, text
import os

# MySQL 连接配置
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = "student_planning"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"

def create_database():
    """创建数据库"""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # 检查数据库是否存在
        result = conn.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}'"))
        if not result.fetchone():
            print(f"创建数据库：{DB_NAME}")
            conn.execute(text(f"CREATE DATABASE `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        else:
            print(f"数据库已存在：{DB_NAME}")

def create_tables():
    """创建表结构"""
    engine = create_engine(f"{DATABASE_URL}{DB_NAME}")

    # 导入所有模型以触发表创建
    from app.models import create_tables as create_app_tables
    create_app_tables()
    print("表结构创建完成！")

def insert_defaults():
    """插入默认数据"""
    engine = create_engine(f"{DATABASE_URL}{DB_NAME}")

    with engine.connect() as conn:
        # 插入默认管理员
        try:
            conn.execute(text("""
                INSERT INTO admins (username, password)
                VALUES ('admin', 'admin123')
                ON DUPLICATE KEY UPDATE username=username
            """))

            # 插入一些默认专业模板
            templates = [
                ("计算机科学与技术",
                 "数据结构、算法、操作系统、计算机网络、数据库原理、软件工程",
                 "软件工程师、算法工程师、架构师、全栈开发",
                 "推荐证书：软件设计师、系统分析师、云计算认证"),

                ("金融学专业",
                 "微观经济学、宏观经济学、金融学、证券投资学、保险学、风险管理",
                 "银行、证券、基金、保险、金融机构管理岗",
                 "推荐证书：证券从业资格证、基金从业资格证、CFA、FRM"),

                ("法学专业",
                 "宪法学、民法学、刑法学、行政法学、诉讼法学、国际法学",
                 "律师、法官、检察官、法务专员、公务员",
                 "推荐证书：法律职业资格证书（法考）"),

                ("英语专业",
                 "综合英语、听力口语、英语写作、英美文学、翻译理论与实践、跨文化交际",
                 "教师、翻译、外贸、跨境电商、外企职员",
                 "推荐证书：英语专业八级 TESOL 教师资格证"),

                ("工商管理",
                 "管理学原理、市场营销、人力资源管理、会计学、战略管理",
                 "企业管理人员、市场营销、人力资源、咨询顾问",
                 "推荐证书：人力资源管理师、PMP 项目管理")
            ]

            for major_name, courses, career, certs in templates:
                conn.execute(text("""
                    INSERT INTO major_templates (major_name, core_courses, career_path, recommended_certificates)
                    VALUES (:name, :courses, :career, :certs)
                    ON DUPLICATE KEY UPDATE major_name=major_name
                """), {
                    "name": major_name,
                    "courses": courses,
                    "career": career,
                    "certs": certs
                })

            conn.commit()
            print("默认数据插入完成！")

        except Exception as e:
            print(f"插入数据时出错：{e}")

if __name__ == "__main__":
    print("开始初始化数据库...")
    create_database()
    create_tables()
    insert_defaults()
    print("数据库初始化完成！🎉")
