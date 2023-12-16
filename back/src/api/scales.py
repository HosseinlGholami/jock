import random
from src.api import scales_crud
from src.api.models import scalesInAdmin, scalesIn, scalesIn, scalesOut
from fastapi import APIRouter, HTTPException, Path, Depends, Request
from typing import List
from src.jwt_token import oauth2_scheme, is_admin

router = APIRouter()


@router.post("/", status_code=201, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_scale_admin(request: Request, payload: scalesInAdmin):
    print(request.state.user)
    scale_id = await scales_crud.postScaleAdmin(payload)
    return await scales_crud.getScale(scale_id)


@router.put("/mac/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def update_scale_mac(request: Request, payload: scalesInAdmin):
    print(request.state.user)
    scale = await scales_crud.getScale_name(payload.name)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    scale_id = await scales_crud.putScaleMac(payload)
    return await scales_crud.getScale(scale_id)


@router.put("/", response_model=scalesOut, status_code=201, dependencies=[Depends(oauth2_scheme)])
async def update_scale_location(request: Request, payload: scalesIn):
    print(request.state.user)
    scale = await scales_crud.getScale_name(payload.name)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    scale_id = await scales_crud.putScaleGate(payload)
    return await scales_crud.getScale(scale_id)


@router.get("/admin/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def read_all_scales_admin(request: Request,):
    print(request.state.user)
    return await scales_crud.getAllScale()


@router.get("/", response_model=List[scalesOut], dependencies=[Depends(oauth2_scheme)])
async def read_all_scales(request: Request,):
    print(request.state.user)
    return await scales_crud.getAllScale()


@router.get("/index/{id}/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def get_scale_id(request: Request, id: int = Path(..., gt=0),):
    print(request.state.user)
    scale = await scales_crud.getScale(id)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    return scale


@router.get("/{name}/", response_model=scalesOut, dependencies=[Depends(oauth2_scheme)])
async def get_scale_name(request: Request, name: str):
    print(request.state.user)
    scale = await scales_crud.getScale_name(name)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    return scale


@router.delete("/{id}/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def delete_scale(request: Request, id: int = Path(..., gt=0)):
    print(request.state.user)
    scale = await scales_crud.getScale(id)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    await scales_crud.deleteScale(id)
    return scale
