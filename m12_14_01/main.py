import asyncio
import re
from ipaddress import ip_address
from typing import Callable

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, BackgroundTasks, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.routes import todos, auth, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]
#
#
# @app.middleware("http")
# async def limit_access_by_ip(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     print(ip)
#     if ip not in ALLOWED_IPS:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
#     response = await call_next(request)
#     return response
#
#
# user_agent_ban_list = [r"Python-urllib"]
#
#
# @app.middleware("http")
# async def user_agent_ban_middleware(request: Request, call_next: Callable):
#     user_agent = request.headers.get("user-agent")
#     print(user_agent)
#     for ban_pattern in user_agent_ban_list:
#         if re.search(ban_pattern, user_agent):
#             return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router, prefix='/api')
app.include_router(users.router, prefix='/api')


async def task():
    await asyncio.sleep(3)
    print("Send email")
    return True


@app.get("/")
async def read_root(background_tasks: BackgroundTasks):
    background_tasks.add_task(task)
    return {"message": "TODO API"}


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", reload=True, log_level="info")
