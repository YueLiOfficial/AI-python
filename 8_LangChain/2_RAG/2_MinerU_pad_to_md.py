import requests
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def upload_pdf_file():
    token = os.getenv("MINERU_API_TOKEN")
    # token = "sk-EN2WnWNOzT1b5ShlsvXs9yNlATwfa1dCX47sW1c43bzTG8A2"
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": [
            {"name":"demo.pdf", "data_id": "abcd"}
        ],
        "model_version":"vlm"
    }

    try:
        # 第一次请求，获取file_url
        response = requests.post(url=url, headers=header, json=data)
        if response.status_code == 200:
            result = response.json()
            if result["code"] == 0:
                batch_id = result["data"]["batch_id"]
                file_url = result["data"]["file_urls"][0]

                # 第二次请求，上传pdf文件
                with open(Path(__file__).parent / "assets" / "sample.pdf", mode="rb") as f:
                    response = requests.put(url=file_url, data=f)
                    if response.status_code == 200:
                        print("文件上传成功")
                        return batch_id
                    else:
                        print("文件上传失败")
            else:
                print(f"获取upload_url失败, 状态码: {result["code"]}, 失败原因: {result["msg"]}")
        else:
            print(f"请求失败, 状态码: {response.status_code}, 失败原因: {response}")

    except Exception as e:
        print({e})

def get_MinerU_result(batch_id):
    token = os.getenv("MinerU_API_TOKEN")
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url=url, headers=header)
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    # batch_id = upload_pdf_file()
    # print(batch_id)
    get_MinerU_result("946d6825-abee-4179-909a-2e1d3ded50f6")