# src/main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api import jocks

# from src.api import ping
from src.db import engine, metadata, database

import os
print(f"==============================>>>>>{os.environ['LOCAL_IP']}")

metadata.create_all(engine)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(jocks.router, prefix="/jocks", tags=["jock-crud"])
