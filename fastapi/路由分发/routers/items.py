from fastapi import FastAPI, APIRouter

router = APIRouter(
    prefix="/item",
    tags=["物品信息"]
)

@router.get("/")
async def get_all_items():
    return {"message": "获取所有物品信息"}

@router.get("/{item_id}")
async def get_item(item_id: int):
    return {"message": f"获取物品ID为{item_id}的物品信息"}
