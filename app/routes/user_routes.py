from fastapi import APIRouter, HTTPException
from services.user_service import create_user, get_user_by_email
from schemas.user_schema import UserCreateSchema

router = APIRouter()


@router.post("/register/")
async def register_user(user: UserCreateSchema):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = await create_user(user)
    return {"message": "User created", "user_id": user_id}
