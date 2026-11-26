
from fastapi import APIRouter, Depends, Response, Request, HTTPException

from auth.permissions import get_current_user
from auth.security import (
    REFRESH_COOKIE_NAME,
    set_refresh_cookie,
    clear_refresh_cookie,
)
from schemas.user import UserRegister, UserLogin
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(body: UserRegister):
    return auth_service.register(
        body.full_name,
        str(body.email),
        body.password,
    )


@router.post("/login")
def login(body: UserLogin, response: Response):
    result, raw_refresh_token, expires_at = auth_service.login(
        str(body.email),
        body.password,
    )

    set_refresh_cookie(response, raw_refresh_token, expires_at)

    print("LOGIN ROUTE EXECUTED")
    print("COOKIE HEADER ADDED:", "set-cookie" in response.headers)

    return result


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user


@router.post("/refresh")
def refresh(request: Request, response: Response):
    raw_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if not raw_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing",
        )

    try:
        access_token, new_refresh_token, expires_at = (
            auth_service.refresh_login(raw_token)
        )
    except HTTPException:
        clear_refresh_cookie(response)
        raise

    set_refresh_cookie(response, new_refresh_token, expires_at)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(request: Request, response: Response):
    raw_token = request.cookies.get(REFRESH_COOKIE_NAME)

    auth_service.logout(raw_token)
    clear_refresh_cookie(response)

    return {"message": "Logged out successfully"}


@router.post("/logout-all")
def logout_all(
    response: Response,
    user: dict = Depends(get_current_user),
):
    auth_service.logout_all(user["id"])
    clear_refresh_cookie(response)

    return {
        "message": "All active sessions have been revoked"
    }
