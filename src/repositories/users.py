from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.db_session.execute(query)
        if (model_ := result.scalars().one_or_none()) is None:
            return None
        else:
            return UserWithHashedPassword.model_validate(model_, from_attributes=True)
