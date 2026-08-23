import asyncio
import aiohttp

async def download_pic(session, url):
    print(f"开始下载{url}")

    # 发送请求，下载图片，请求发送后，需要等待服务器返回数据，等待的时间就是I/O等待
    response = await session.get(url)
    # 等待数据，图片可能被分段传输，需要等待数据读完，等待的时间也是I/O等待
    content = await response.read()

    print("下载完毕")

    with open(url[-10:], 'wb') as f:
        f.write(content)

    response.release()

async def main():

    url_list = [
        'https://n.sinaimg.cn/spider20260129/217/w600h417/20260129/3e26-917ee55a8a42b8626807c332c24981de.png',
        'https://n.sinaimg.cn/finance/transform/97/w630h267/20260129/97c4-b211cc51784830f09ee19e450475c93b.png',
        'https://n.sinaimg.cn/spider20260129/539/w1439h700/20260129/e09a-cc2ca319e00f701ccfca3ebc62aa8772.png'
    ]

    # 创建会话
    session = aiohttp.ClientSession()

    # 创建协程对象
    coroutine_list = [download_pic(session, url) for url in url_list]
    # asyncio.gather()能够一次性将多个协程对象包装成事件循环任务并添加到事件循环中
    await asyncio.gather(*coroutine_list)

    # 关闭会话
    await session.close()

asyncio.run(main())