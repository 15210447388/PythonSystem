"""
异常全局处理
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from app.common.logger import log


# 自定义业务异常
class BusinessException(HTTPException):
    def __init__(self, code: int = 400, msg: str = "请求异常"):
        sum().__init__(status_code=code, detail=msg)


# 注册全局异常处理器
def register_exception_handler(app: FastAPI):
    #捕获HTTP异常
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        log.error(f"HTTP异常:{exc.status_code} | {exc.detail}")
        return JSONResponse(status_code=exc.status_code,
                            content={"code": exc.status_code, "message": exc.detail, "data": None})
    #捕获全局未知异常
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log.error(f"系统未知异常: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "服务器内部错误", "data": None}
        )
