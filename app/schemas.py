"""
与API交互数据校验&响应模型 分页 搜索
= Field(....)设置参数的校验
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


# 分页通用入参
class PageParam(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页条数")  # 最大100一页
    keyword: Optional[str] = Field(None, description="模糊搜索关键词")
    order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="排序：asc/desc")


# =======================用户==================
class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50, description="用户名")
    password: str = Field(min_length=6, max_length=72, description="密码，最长72位")


class UserInfo(BaseModel):
    id: int
    username: str
    avatar: Optional[str] = ""
    credits: Optional[int] = 0
    create_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# ==================== 帖子 ====================
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None

class PostInfo(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    create_time: datetime
    update_time: datetime
    class Config:
        orm_mode = True


# ==================== 评论 ====================
class CommentCreate(BaseModel):
    post_id: int
    content: str = Field(min_length=1)


class CommentInfo(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    create_time: datetime

    class Config:
        orm_mode = True


# ==================== 点赞 ====================
class LikeCreate(BaseModel):
    post_id: int
