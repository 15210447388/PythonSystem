from sqlalchemy.orm import Session
from app import models, schemas

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(title=post.title, content=post.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = get_post_by_id(db, post_id)
    if not db_post:
        return None
    if post_update.title is not None:
        db_post.title = post_update.title
    if post_update.content is not None:
        db_post.content = post_update.content
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post_list(db: Session, params: schemas.PageParams):
    query = db.query(models.Post)
    if params.keyword:
        query = query.filter(models.Post.title.like(f"%{params.keyword}%"))
    if params.order == "desc":
        query = query.order_by(models.Post.create_time.desc())
    else:
        query = query.order_by(models.Post.create_time.asc())
    skip = (params.page - 1) * params.page_size
    return query.offset(skip).limit(params.page_size).all()

def delete_post(db: Session, post_id: int):
    post = get_post_by_id(db, post_id)
    if post:
        db.delete(post)
        db.commit()
    return post