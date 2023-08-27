import random
from src.api import scales_crud, weight_crud
from src.api.models import scalesInAdmin, scalesIn, scalesIn, scalesOut
from fastapi import APIRouter, HTTPException, Path, Depends, Request
from src.jwt_token import oauth2_scheme
from datetime import datetime

router = APIRouter()


@router.get("/{name}/", dependencies=[Depends(oauth2_scheme)])
async def get_scale_name(request: Request, name: str):
    scale = await scales_crud.getScale_name(name)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    user_id = request.state.user["id"]
    weight_id = await weight_crud.postWeight(user_id, scale.id, scale.name)
    return await weight_crud.getWeight(weight_id)


@router.get("/{gate_id}/", dependencies=[Depends(oauth2_scheme)])
async def get_scale_gate_id(request: Request, gate_id: str):
    scale = await scales_crud.getScale_gateid(gate_id)
    if not scale:
        raise HTTPException(status_code=404, detail="scale not found")
    user_id = request.state.user["id"]
    weight_id = await weight_crud.postWeight(user_id, scale.id, scale.name)
    return await weight_crud.getWeight(weight_id)
