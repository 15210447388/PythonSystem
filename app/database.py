from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 数据库连接地址
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ORM 基类
Base = declarative_base()

# 数据库会话依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()