from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

items_list = [{"item1": "Foo"}, {"item2": "Bar"}, {"item3": "Baz"}]

@app.get("/")
async def hello():
    return {"message": "hello world"}

# name为路径参数，是必填的, 可以声明路径参数的类型，如果传的类型不一致则报错, 路径参数可以使用Path()添加注解
@app.get("/chat/{name}")
async def say_hello(name: str = Path(..., description="say_hello", min_length=2, max_length=5)):
    return {"message": f"hello {name}"}

# 没有在路径中的参数是查询参数，查询参数跟在?后面，使用&分隔, 查询参数可以使用Query()添加注解
# http://127.0.0.1:8000/item?start=0&limit=2
@app.get("/item")
async def read_item_required(
    start: int = Query(0, description="开始索引"), 
    limit: int = Query(1, description="取的元素数量")
    ):
    return items_list[start: start + limit]

# 如果查询参数写了默认值，则可以不指定查询参数
@app.get("/item_default")
async def read_item_default(start: int = 0, limit: int = 10):
    return items_list[start: start + limit]

# 查询参数可以设置为可选的，如果不知道设置什么默认值，可以设置为None
# 查询参数也可以是bool类型，true、yse、on、1都表示真
@app.get("/items_optional/{item_id}")
async def read_item_optional(item_id: int, q: str | None = None, short: bool = False):
    item = items_list[item_id]
    if q:
        item.update({"q": q})

    if short:
        item.update({"message": "这是物品描述信息"})

    return item

# 多个路径参数, read_user_item()中声明的参数顺序和url的路径参数顺序不一样也可以正常运行
@app.get("/user/{user_id}/items/{item_id}")
async def read_user_item(item_id: int, user_id: int):
    item = {"item": items_list[item_id], "user": user_id}
    return item

# 请求传参，一般配POST, PUT使用

# 定义参数体, 属性可以使用Field添加注解
class Item(BaseModel):
    item_name: str = Field(..., description="物品名称")
    price: float = Field(..., description="物品价格", gt=0)

@app.post("/add_item")
async def add_item(item: Item):
    return item