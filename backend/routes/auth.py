from fastapi import APIRouter, Depends, Request, Response

from auth.permissions import get_current_user
from auth.request_info import get_client_info, set_refresh_cookie, clear_refresh_cookie
from config.settings import REFRESH_COOKIE_NAME
from schemas.user import UserRegister, UserLogin
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(body: UserRegister, request: Request):
    ip, ua = get_client_info(request)
    return auth_service.register(body.full_name, str(body.email), body.password, ip, ua)


@router.post("/login")
def login(body: UserLogin, request: Request, response: Response):
    ip, ua = get_client_info(request)
    result, raw_refresh = auth_service.login(str(body.email), body.password, ip, ua)
    set_refresh_cookie(response, raw_refresh)
    return result


@router.post("/refresh")
def refresh(request: Request, response: Response):
    ip, ua = get_client_info(request)
    raw = request.cookies.get(REFRESH_COOKIE_NAME)
    result, new_raw = auth_service.refresh(raw, ip, ua)
    set_refresh_cookie(response, new_raw)
    return result


@router.post("/logout")
def logout(request: Request, response: Response):
    ip, ua = get_client_info(request)
    result = auth_service.logout(request.cookies.get(REFRESH_COOKIE_NAME), ip, ua)
    clear_refresh_cookie(response)
    return result


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user