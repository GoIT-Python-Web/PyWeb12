import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes import todos, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(todos.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "TODO API"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", reload=True, log_level="info")
