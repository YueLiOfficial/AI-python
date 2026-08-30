from fastapi import FastAPI, APIRouter

router = APIRouter(
    prefix="/user",
    tags=["用户信息"]
)

@router.get("/")
async def get_all_users():
    return {"message": "获取所有用户列表"}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"message": f"获取用户ID为{user_id}的用户信息"}