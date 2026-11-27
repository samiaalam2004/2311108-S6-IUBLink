from fastapi import APIRouter, Depends, Request, Response

from auth.permissions import get_current_user
from auth.request_info import get_client_info, clear_refresh_cookie
from config.settings import REFRESH_COOKIE_NAME
from schemas.user import ProfileUpdate, ChangePassword
from services import user_service

router = APIRouter(prefix="/api/users/me", tags=["users"])


@router.patch("")
def update_profile(body: ProfileUpdate, request: Request,
                   user: dict = Depends(get_current_user)):
    ip, ua = get_client_info(request)
    return user_service.update_profile(user, body.model_dump(exclude_unset=True), ip, ua)


@router.post("/change-password")
def change_password(body: ChangePassword, request: Request, response: Response,
                    user: dict = Depends(get_current_user)):
    ip, ua = get_client_info(request)
    result = user_service.change_password(
        user, body.current_password, body.new_password, ip, ua)
    clear_refresh_cookie(response)
    return result


@router.get("/sessions")
def list_sessions(request: Request, user: dict = Depends(get_current_user)):
    return user_service.list_sessions(user["id"], request.cookies.get(REFRESH_COOKIE_NAME))


@router.delete("/sessions/{session_id}")
def revoke_session(session_id: int, request: Request,
                   user: dict = Depends(get_current_user)):
    ip, ua = get_client_info(request)
    return user_service.revoke_session(user, session_id, ip, ua)