import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.security import decode_access_token
from crud import user_crud

bearer_scheme = HTTPBearer()


class Role:
    USER = "user"
    ADMIN = "admin"


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    unauthorized = HTTPException(
        status_code=401, detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = int(decode_access_token(credentials.credentials)["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise unauthorized

    user = user_crud.get_by_id(user_id)
    if user is None:
        raise unauthorized
    if user["is_banned"]:
        raise HTTPException(status_code=403, detail="Your account has been banned")
    return user


def require_role(*allowed_roles: str):
    def checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
        return current_user
    return checker