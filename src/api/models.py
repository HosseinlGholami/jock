from pydantic import BaseModel, Field, NonNegativeInt
from datetime import datetime as dt
from pytz import timezone as tz


class JockSchema(BaseModel):
    # additional validation for the inputs
    author: str = Field(..., min_length=3, max_length=50)
    text: str = Field(..., min_length=3, max_length=300)
    approved: bool = "False"
    created_date: str = dt.now(tz("Asia/Tehran")).strftime("%Y-%m-%d %H:%M")


class JockDB(JockSchema):
    id: int
