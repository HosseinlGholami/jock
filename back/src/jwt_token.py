
from typing import Optional
import jwt
import os
from datetime import datetime, timedelta
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from starlette.requests import Request
from src.api import user_crud
from fastapi import exceptions
from src.db import Role


def is_admin(request: Request):
    user = request.state.user
    if not user["role"] == Role.admin:
        raise exceptions.HTTPException(
            403, "You do not have permisson for this resource")


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, os.environ['JWT_SECRET'], algorithms=["HS256"])
            user = await user_crud.getUser(payload["sub"])
            request.state.user = user
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise exceptions.HTTPException(401, "Invalid token")
        except Exception as e:
            raise e


oauth2_scheme = CustomHTTPBearer()


def create_access_token(user):
    try:
        payload = {"sub": user["id"]}
        # , "exp": datetime.utcnow() +timedelta(minutes=5)}
        return jwt.encode(payload, os.environ['JWT_SECRET'], algorithm="HS256")
    except Exception as ex:
        raise exceptions.HTTPException(401, "Invalid token")
