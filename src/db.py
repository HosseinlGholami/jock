# src/db.py

import sqlalchemy as db
import os

from sqlalchemy import (Column, Integer, String,
                        Table, create_engine, MetaData)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz

load_dotenv()

# DATABASE_URL = f"mysql+mysqlconnector://root:root@{os.environ['LOCAL_IP']}:3306/jock-app-db"
DATABASE_URL = f"mysql+mysqlconnector://root:root@172.20.47.89:3306/jock-app-db"


# SQLAlchemy
engine = db.create_engine(DATABASE_URL)
metadata = MetaData()
jocks = Table(
    "jocks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("author", String(50)),
    Column("text", String(300)),
    Column("approved", String(8), default="False"),
    Column("created_date", String(50), default=dt.now(
        tz("Asia/Tehran")).strftime("%Y-%m-%d %H:%M"))
    # Column("likes", Integer, default=0, nullable=False),
    # Column("dislikes", Integer, default=0, nullable=False),
)

# Databases query builder
database = Database(DATABASE_URL)
