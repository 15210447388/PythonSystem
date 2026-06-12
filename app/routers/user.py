"""
用户API
"""
from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.common.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.crud import user as user_crud
from app.database import get_db

# 根路由
router = APIRouter(prefix="/user", tags=["用户管理"])
"""
用户注册
"""


@router.post("/register", response_model=schemas.UserInfo, summary="用户注册")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 判断是用户否存在
    exit_user = user_crud.get_user_by_username(db, username=user.username)
    if exit_user:
        raise HTTPException(status_codes=400, detail="用户已存在")
    return user_crud.create_user(db, user)


"""
#用户登录返回token
"""


@router.post("/login", response_model=schemas.Token, summary="用户登录获取Token")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    # 用表单里的 username/password 去校验
    user_db = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user_db:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 生成Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_db.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


"""
获取用户列表
"""


@router.get("/", response_model=list[schemas.UserInfo], summary="用户列表（分页+搜索+排序）")
def list_users(params: schemas.PageParam = Depends(), db: Session = Depends(get_db)):
    return user_crud.get_user_list(db, params)


"""
根据用户低查询用户详情
"""


@router.get("/{user_id}", response_model=schemas.UserInfo, summary="根据用户低查询用户详情")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_codes=404, detail="用户不存在")
    return user


"""
删除用户
"""


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not user_crud.delete_user(db, user_id=user_id):
        raise HTTPException(status_codes=404, detail="用户不存在")
    return {"msg": "删除成功"}
