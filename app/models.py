"""
数据库模型实体
主键 通过primary_key=true设置
是否是索引：index=True
是否可以为空：nullable=False
获取当前时间：default=func.now()
自动递增：autoincrement=True
表与表直接的关联：ForeignKey("users.id")
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base

#用户表
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # 用户id 主键 自动递增
    username = Column(String(50), nullable=False, unique=True, comment="用户名")
    password = Column(String(100),nullable=False,comment="加密密码")
    crate_time = Column(DateTime, default=func.now(), nullable=False)
#贴子表
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100),nullable=False,comment="标题")
    content =Column(Text,nullable=False,comment="内容")
    user_id = Column(Integer,ForeignKey("user.id"),nullable=False,comment="作者ID与用户表关联")
    create_time = Column(DateTime,default=func.now(),nullable=False)
    update_time = Column(DateTime,default=func.now(),onupdate=func.now(),nullable=False)
# 点赞表
class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    create_time = Column(DateTime, default=func.now())
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uix_post_user_like"),)

# 评论表
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False, comment="帖子ID")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="评论用户ID")
    content = Column(Text, nullable=False, comment="评论内容")
    create_time = Column(DateTime, default=func.now())