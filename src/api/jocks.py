from src.api import crud
from src.api.models import JockDB, JockSchema
from fastapi import APIRouter, HTTPException, Path
from typing import List
from datetime import datetime as dt
router = APIRouter()


@router.post("/", response_model=JockDB, status_code=201)
async def create_jocks(payload: JockSchema):
    jock_id = await crud.post(payload)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    response_object = {
        "id": jock_id,
        "author": payload.author,
        "text": payload.text,
        "approved": payload.approved,
        "created_date": created_date,
    }
    return response_object


@router.get("/{id}/", response_model=JockDB)
async def read_jock(id: int = Path(..., gt=0),):
    jock = await crud.get(id)
    if not jock:
        raise HTTPException(status_code=404, detail="jock not found")
    return jock


@router.get("/", response_model=List[JockDB])
async def read_all_jocks():
    return await crud.get_all()


@router.put("/{id}/", response_model=JockDB)
# Ensures the input is greater than 0
async def update_jock(payload: JockSchema, id: int = Path(..., gt=0)):
    jock = await crud.get(id)
    if not jock:
        raise HTTPException(status_code=404, detail="jock not found")
    jock_id = await crud.put(id, payload)
    response_object = {
        "id": jock_id,
        "author": payload.author,
        "text": payload.text,
        "approved": payload.approved,
    }
    return response_object


@router.delete("/{id}/", response_model=JockDB)
# DELETE route
async def delete_jock(id: int = Path(..., gt=0)):
    jock = await crud.get(id)
    if not jock:
        raise HTTPException(status_code=404, detail="jock not found")
    await crud.delete(id)

    return jock
