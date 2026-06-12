"""
用户的增删改查方法
"""
from sqlalchemy.orm import Session
from app import  models,schemas
from app.common.auth import get_password_hash,verify_password

def create_user(db: Session,user: schemas.UserCreate):
    #密码加密
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username,password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session,user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session,username: str):
    return db.query(models.User).filter(models.User.username == username).first()
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
def get_user_list(db: Session, params:schemas.PageParam):
    query = db.query(models.User)
    if params.keyword:
        query = query.filter(models.User.username.ilike(f"%{params.keyword}%"))
    if params.order:
        query = query.order_by(models.User.crate_time.desc())
    else:
        query = query.order_by(models.User.crate_time.asc())
    skip = (params.page-1) * params.page_size
    return query.offset(skip).limit(params.page_size).all()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


