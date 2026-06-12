# 日志配置
import os
import sys

import logger

# 日志记录
log_path = "logs"  # 日志存放的路径
if not os.path.exists(log_path):
    os.makedirs(log_path)
# 移除默认handler
logger.remove()
# 控制台输出
logger.add(sys.stdout, format("{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"),
           level="INFO")
# 文件日志，按日期分割
logger.add(
    f"{log_path}/app.log",
    rotation="00:00",
    retention="7 days",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="INFO"
)
# 对外导出
log = logger
