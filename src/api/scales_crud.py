from src.api.models import scalesInAdmin, scalesIn
from src.db import scales, database
from datetime import datetime


async def postScaleAdmin(payload: scalesInAdmin):
    query = scales.insert().values(
        name=payload.name,
        mac=payload.mac,
    )
    return await database.execute(query=query)


async def putScaleMac(payload: scalesInAdmin):
    query = (
        scales.update().where(payload.name == scales.c.name).values(
            mac=payload.mac)
    )
    return await database.execute(query=query)


async def putScaleGate(payload: scalesIn):
    query = (
        scales.update().where(payload.name == scales.c.name).values(
            gate_id=payload.gate_id)
    )
    return await database.execute(query=query)


async def getScale(id: int):
    query = scales.select().where(id == scales.c.id)
    return await database.fetch_one(query=query)


async def getScale_name(name: str):
    query = scales.select().where(name == scales.c.name)
    return await database.fetch_one(query=query)


async def getScale_gateid(gateid: int):
    query = scales.select().where(gateid == scales.c.gate_id)
    return await database.fetch_one(query=query)


async def getAllScale():
    query = scales.select()
    return await database.fetch_all(query=query)


async def deleteScale(id: int):
    query = scales.delete().where(id == scales.c.id)
    return await database.execute(query=query)
