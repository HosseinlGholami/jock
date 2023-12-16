# src/main.py

import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api import users, scales, weight

from src.db import database

from src import ip
MY_IP = ip.get_local_ip()

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

app.include_router(scales.router, prefix="/scales", tags=["scales-crud"])
app.include_router(users.router,  prefix="/users", tags=["users-crud"])
app.include_router(weight.router,  prefix="/weight", tags=["weight-crud"])
