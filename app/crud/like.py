"""
点赞的增删改 分页 搜索
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas

#点赞
def create_like(db: Session, post_id: int, user_id: int):
    try:
        db_like = models.Like(post_id=post_id, user_id=user_id)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like
    except IntegrityError:
        db.rollback()
        return None
#取消点赞 防止重复点赞
def delete_like(db: Session, post_id: int, user_id: int):
    like = db.query(models.Like).filter(
        models.Like.post_id == post_id, models.Like.user_id == user_id
    ).first()
    if like:
        db.delete(like)
        db.commit()
    return like

def get_post_like_count(db: Session, post_id: int):
    return db.query(models.Like).filter(models.Like.post_id == post_id).count()