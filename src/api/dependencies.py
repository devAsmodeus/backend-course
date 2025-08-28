from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing_extensions import Annotated

from src.database import async_session_maker
from src.utils.db_manager import DBManager
from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(default=None, description="Количество отелей на странице", ge=1, le=10)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(
        request: Request
) -> str:
    if access_token := request.cookies.get('access_token'):
        return access_token
    else:
        raise HTTPException(status_code=401, detail="User unauthorized")


def get_current_user_id(
        access_token: str = Depends(get_token)
) -> int:
    data = AuthService().decode_token(access_token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
