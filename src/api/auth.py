from fastapi import APIRouter, Response

from src.exceptions import (
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestedAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestedAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    return {"message": "Complete"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestedAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    return await AuthService(db).get_one_or_none_user(user_id=user_id)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Complete"}
