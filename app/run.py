import uvicorn

from fastapi import FastAPI
from v1.routes import router
from v1.config import conn

app=FastAPI()

app.include_router(router, prefix="/api/v1")


if __name__=="__main__":
    uvicorn.run("run:app",host="127.0.0.1",port=8000,reload=True)
