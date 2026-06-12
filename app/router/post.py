"""
帖子管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.common.auth import get_current_user_id
from app.database import get_db
from app.crud import post as post_crud

router = APIRouter(prefix="/post", tags=["帖子管理"])

"""
发布帖子(需要登录)
"""


@router.post("/", response_model=schemas.PostInfo, summary="发布帖子(需要登录)")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user_id: int = Depends(get_current_user_id)):
    return post_crud.create_post(db, post,user_id=current_user_id)


"""
获取帖子
"""


@router.get("/{post_id}", response_model=schemas.PostInfo, summary="获取帖子")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_crud.get_post_by_id(db, post_id = post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    return post


"""
修改帖子
"""


@router.put("/{post_id}", response_model=schemas.PostInfo, summary="修改帖子（需要登录）")
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db),
                current_user_id: int = Depends(get_current_user_id)):
    post = post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    if post.user_id != current_user_id:
        raise HTTPException(status_code=401, detail="无权限修改")
    return post_crud.update_post(db,post_id, post_update)


"""
帖子列表
"""


@router.post("/list", response_model=list[schemas.PostInfo], summary="帖子列表 分页+搜索+排序")
def list_post(params: schemas.PageParam, db: Session = Depends(get_db)):
    return post_crud.get_post_list(db, params)


"""
删除帖子需要登录
"""


@router.delete("/{post_id}", summary="删除帖子（需要登录）")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    # 判断帖子是否存在
    post = post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    if post.user_id != current_user_id:
        raise HTTPException(status_code=401, detail="无权限删除")
    post_crud.delete_post(db, post_id)
    return {"msg": "删除成功"}
