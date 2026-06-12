"""
点赞管理API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import like as like_crud
from app.database import get_db
from app.common.auth import get_current_user_id

router = APIRouter(prefix="/likes", tags=["点赞管理"])


@router.post("/", summary="点赞(需登录)")
def like_post(
        data: schemas.LikeCreate,
        db: Session = Depends(get_db),
        uid: int = Depends(get_current_user_id)
):
    res = like_crud.create_like(db, data.post_id, uid)
    if not res:
        raise HTTPException(status_code=400, detail="已点赞或帖子不存在")
    return {"msg": "点赞成功"}


@router.delete("/", summary="取消点赞(需登录)")
def cancel_like(
        post_id: int,
        db: Session = Depends(get_db),
        uid: int = Depends(get_current_user_id)
):
    if not like_crud.delete_like(db, post_id, uid):
        raise HTTPException(status_code=404, detail="点赞记录不存在")
    return {"msg": "取消点赞成功"}


@router.get("/count/{post_id}", summary="获取帖子点赞数")
def get_count(post_id: int, db: Session = Depends(get_db)):
    count = like_crud.get_post_like_count(db, post_id)
    return {"post_id": post_id, "like_count": count}
