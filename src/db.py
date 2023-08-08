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

DATABASE_URL = f"mysql+mysqlconnector://root:root@{os.environ['LOCAL_IP']}:3306/sca-app-db"


# SQLAlchemy
engine = db.create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed", String(8), default="False"),
    Column("created_date", String(50), default=dt.now(
        tz("Asia/Tehran")).strftime("%Y-%m-%d %H:%M"))
)

# Databases query builder
database = Database(DATABASE_URL)
