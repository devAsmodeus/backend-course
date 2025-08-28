from fastapi import APIRouter, HTTPException, Response

from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestedAdd, UserAdd


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"]
)


@router.post("/register")
async def register_user(
        db: DBDep,
        data: UserRequestedAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password
    )
    await db.users.add(new_user_data)
    await db.commit()

    return {"message": "Complete"}


@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserRequestedAdd,
        response: Response
):
    user = await db.users.get_user_with_hashed_password(
        email=data.email
    )
    if not user:
        raise HTTPException(status_code=401, detail="User unauthorized")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password incorrect")

    access_token = AuthService().create_access_token({"user_id": user.id})

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(
        id=user_id
    )
    return user


@router.post("/logout")
async def logout_user(
        response: Response
):
    response.delete_cookie(key="access_token")
    return {"message": "Complete"}
