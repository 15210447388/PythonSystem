"""
评论的增删改 分页 搜索
"""

from sqlalchemy.orm import Session
from app import models, schemas

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(
        post_id=comment.post_id,
        user_id=user_id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment_list(db: Session, post_id: int, params: schemas.PageParams):
    query = db.query(models.Comment).filter(models.Comment.post_id == post_id)
    if params.order == "desc":
        query = query.order_by(models.Comment.create_time.desc())
    else:
        query = query.order_by(models.Comment.create_time.asc())
    skip = (params.page - 1) * params.page_size
    return query.offset(skip).limit(params.page_size).all()

def delete_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment