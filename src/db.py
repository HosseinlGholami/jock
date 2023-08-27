# src/db.py

import sqlalchemy as db
import os

from sqlalchemy import (Column, Integer, String, Enum,
                        Table, MetaData, ForeignKey)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz

import enum

load_dotenv()

# DATABASE_URL = f"mysql+mysqlconnector://root:root@{os.environ['LOCAL_IP']}:3306/joke-app-db"
DATABASE_URL = f"mysql+mysqlconnector://root:root@172.20.44.69:3306/joke-app-db"

# SQLAlchemy
metadata = MetaData()

scales = Table(
    "scale_entity",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False, unique=True),
    Column("mac", String(300), nullable=False),
    Column("gate_id", Integer, nullable=True),
)


class Role(enum.Enum):
    admin = "admin"
    supernova = "supernova"


users_table = Table(
    "users_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user", String(50), unique=True),
    Column("pswd", String(50)),
    Column("role", Enum(Role), default=""),
    Column("token", String(300), default="", nullable=True),
)


scales_weight = Table(
    "scales_weight",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users_table.id"), nullable=False),
    Column("scale_id", ForeignKey("scale_entity.id"), nullable=False),
    Column("weight", String(300), nullable=False),
    Column("timestamp", String(50), default=dt.now(
        tz("Asia/Tehran")).strftime("%Y-%m-%d %H:%M")),
    # TODO: latancy
)

# Databases query builder
database = Database(DATABASE_URL)
