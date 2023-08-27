from pydantic import BaseModel, Field, NonNegativeInt, validator
from datetime import datetime as dt
from pytz import timezone as tz
from typing import Optional
from datetime import datetime
from src.db import Role


class scalesSchema(BaseModel):
    name: str


class scalesInAdmin(scalesSchema):
    mac: str


class scalesIn(scalesSchema):
    gate_id: Optional[int]


class scalesOut(scalesSchema):
    gate_id: Optional[int]


class scales_weightSchema(BaseModel):
    scale_id: int
    name: str
    weight: str


class userSchema(BaseModel):
    user:  str


class userDBIn(userSchema):
    pswd: str
    role: Role
    token: str


class userDBOut(userSchema):
    pswd: str
    role: str


class userSignOut(userSchema):
    token: str


class userSignIn(userSchema):
    pswd: str


class weightIn(userSchema):
    scale_id: int
    user_id: int
    weight: int
    timestamp: datetime
