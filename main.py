import uvicorn
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import user, post, like,comment

# 程序启动时自动创建所有数据表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="发帖系统", version="1.0")

# 注册所有模块路由
app.include_router(user.router)
app.include_router(post.router)
app.include_router(like.router)
app.include_router(comment.router)

# 根路径测试
@app.get("/")
def root():
    return {"message": "发帖系统运行正常，接口文档：/docs"}

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["."]
    )