from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import PlainTextResponse

from agent import AGENTS
from web.routers import *


# ========================= 生命周期事件 =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期：
    - 启动时：调用所有智能体的 init() 初始化方法
    - 关闭时：按初始化的逆序调用所有智能体的 destroy() 销毁方法
    """
    # 启动事件：初始化所有 Agent
    for item in AGENTS.values():
        await item.init()

    yield

    # 关闭事件：销毁所有 Agent
    for item in reversed(list(AGENTS.values())):
        await item.destroy()


# ========================= 创建 FastAPI 实例 =========================
app = FastAPI(
    title="Agent Center Web Server",
    description="黑马程序员智能体中心",
    lifespan=lifespan
)


# ========================= 异常处理 =========================
def system_exception_handler(req: Request, exc: Exception):
    """
    全局异常处理函数，将异常转换为 500 响应
    """
    return PlainTextResponse(
        content=str(exc),
        status_code=500
    )


# 添加全局异常处理器
app.add_exception_handler(Exception, system_exception_handler)

# ========================= 路由注册 =========================
# 将各个子路由模块挂载到不同前缀下
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(session_router, prefix="/session", tags=["session"])

