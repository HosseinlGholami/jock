from src.api.models import JockSchema
from src.db import jocks, database
from datetime import datetime as dt


async def post(payload: JockSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = jocks.insert().values(author=payload.author,
                                  text=payload.text, approved=payload.approved,
                                  created_date=created_date)
    return await database.execute(query=query)


async def get(id: int):
    query = jocks.select().where(id == jocks.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = jocks.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload=JockSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = (
        jocks.update().where(id == jocks.c.id).values(author=payload.author,
                                                      text=payload.text,
                                                      approved=payload.approved,
                                                      created_date=created_date)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = jocks.delete().where(id == jocks.c.id)
    return await database.execute(query=query)
