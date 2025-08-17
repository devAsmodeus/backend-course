from fastapi import APIRouter

from src.schemas.users import UserRequestedAdd, UserAdd
from src.repositories.users import UsersRepository
from src.database import async_session_maker


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"]
)



@router.post("/register")
async def register_user(
        data: UserRequestedAdd
):
    hashed_password = '121212'
    new_user_data = UserAdd(email=data.email, hased_password=hashed_password)
    async with async_session_maker() as db_session:
        await UsersRepository(db_session).add(new_user_data)
        await db_session.commit()

    return {"message": "Complete"}

