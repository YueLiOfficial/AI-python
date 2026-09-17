from fastapi import FastAPI
import uvicorn

from web.schema import Product
from web.service import TitlePredictService


app = FastAPI()

# 创建服务
service = TitlePredictService()

@app.post("/predict")
def predict(product: Product):
    res = service.predict_classification(product.title)

    return {"商品名称": product.title, "类别": res}

def run_server():
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    run_server()