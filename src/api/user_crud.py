from src.api.models import userDBIn
from src.db import users_table, database
from datetime import datetime


async def postUser(payload: userDBIn):
    query = users_table.insert().values(user=payload.user,
                                        pswd=payload.pswd,
                                        role=payload.role
                                        )
    return await database.execute(query=query)


async def getUser(id: int):
    query = users_table.select().where(id == users_table.c.id)
    return await database.fetch_one(query=query)


async def getUserByName(user: str):
    query = users_table.select().where(user == users_table.c.user)
    return await database.fetch_one(query=query)


async def getAllUser():
    query = users_table.select()
    return await database.fetch_all(query=query)


async def putUser(id: int, payload: userDBIn):
    query = users_table.update().where(id == users_table.c.id).values(user=payload.user,
                                                                      pswd=payload.pswd,
                                                                      role=payload.role,
                                                                      token=payload.token
                                                                      )
    return await database.execute(query=query)


async def putUserToken(id: int, token: str):
    query = users_table.update().where(id == users_table.c.id).values(token=token
                                                                      )
    return await database.execute(query=query)


async def deleteUser(id: int):
    query = users_table.delete().where(id == users_table.c.id)
    return await database.execute(query=query)
