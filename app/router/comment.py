"""
评论管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas,models
from app.crud import comment as comment_crud
from app.database import get_db
from app.common.auth import get_current_user_id

router = APIRouter(prefix="/comments", tags=["评论管理"])

@router.post("/", response_model=schemas.CommentInfo, summary="发表评论(需登录)")
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    uid: int = Depends(get_current_user_id)
):
    return comment_crud.create_comment(db, comment, uid)

@router.get("/post/{post_id}", response_model=List[schemas.CommentInfo], summary="帖子评论列表")
def list_comments(
    post_id: int,
    params: schemas.PageParam = Depends(),
    db: Session = Depends(get_db)
):
    return comment_crud.get_comment_list(db, post_id, params)

@router.delete("/{comment_id}", summary="删除评论(需登录)")
def del_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    uid: int = Depends(get_current_user_id)
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    if comment.user_id != uid:
        raise HTTPException(status_code=403, detail="无权限")
    comment_crud.delete_comment(db, comment_id)
    return {"msg": "删除成功"}