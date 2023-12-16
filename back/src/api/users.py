import random
from src.api import user_crud
from src.api.models import userDBIn, userSignOut, userSignIn
from fastapi import APIRouter, HTTPException, Path, Depends, Request, exceptions
from typing import List
from src.jwt_token import create_access_token, oauth2_scheme, is_admin


router = APIRouter()


@router.post("/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def create_user(request: Request, payload: userDBIn):
    print(request.state.user)
    user_id = await user_crud.postUser(payload)
    return await user_crud.getUser(user_id)


@router.get("/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def read_all_user(request: Request):
    print(request.state.user)
    return await user_crud.getAllUser()


@router.get("/{id}/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def read_user(request: Request, id: int = Path(..., gt=0),):
    user = await user_crud.getUser(id)
    print(request.state.user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.put("/{id}/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def update_user(request: Request, payload: userDBIn, id: int = Path(..., gt=0)):
    print(request.state.user)
    user = await user_crud.getUser(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user_id = await user_crud.putUser(id, payload)
    return await user_crud.getUser(user_id)


@router.delete("/{id}/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
# DELETE route
async def delete_user(request: Request, id: int = Path(..., gt=0)):
    print(request.state.user)
    user = await user_crud.getUser(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    await user_crud.deleteUser(id)
    return user


@router.put("/login", response_model=userSignOut)
async def login_user(userIn: userSignIn):
    user = await user_crud.getUserByName(userIn.user)
    if user == None:
        raise exceptions.HTTPException(401, "user not found...")
    if not user["pswd"] == userIn.pswd:
        raise exceptions.HTTPException(401, "bad password ...")
    token = create_access_token(user)
    await user_crud.putUserToken(user["id"], token)
    return await user_crud.getUser(user["id"])
