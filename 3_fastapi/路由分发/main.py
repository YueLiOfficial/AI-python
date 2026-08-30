from fastapi import FastAPI, APIRouter
from routers import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def hello():
    return {"message": "hello world"}
