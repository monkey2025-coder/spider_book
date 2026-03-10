import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures
import logging


logging.basicConfig(filename='spider_book.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                encoding='utf-8')
logger = logging.getLogger(__name__)

# 三个状态 已完成 未完成 只完成了一部分 0 1 2

with open("Chapters.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_chapter_content(url):
    base_url = url.replace(".html", "")
    total_content = []

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.info(f'1 {url}')
        return len(f"失败 {url}") 

    soup = BeautifulSoup(response.text, 'html.parser')
    chapter_title = soup.find('h1', class_='title').text.strip()

    content = soup.find('div', class_='content')
    for p in content.find_all('p'):
        total_content.append(p.text.strip())
    
    time.sleep(1)  # 避免过快请求导致被封禁

    if "下一页" in response.text:
        for i in range(2, 1000000):
            next_url = f"{base_url}_{i}.html"
            next_response = requests.get(next_url, headers=headers)
            if next_response.status_code != 200:
                logger.info(f'2 {next_url}')
                break
            next_soup = BeautifulSoup(next_response.text, 'html.parser')
            content = next_soup.find('div', class_='content')
            for p in content.find_all('p'):
                total_content.append(p.text.strip())

            time.sleep(1) 
            if "下一页" not in next_response.text:
                break
    
    with open(f"./小说本体/{chapter_title}.txt", "w", encoding="utf-8") as f:
        f.write(chapter_title + "\n\n")
        f.write("\n".join(total_content))

    print(f"已完成章节: {chapter_title}")
    logger.info(f'0 {chapter_title}')

    return len(chapter_title)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    future_to_url = {executor.submit(get_chapter_content, url): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, data))


""" 
Traceback (most recent call last):
  File "/data/spider_book/demo.py", line 70, in <module>
    print('%r page is %d bytes' % (url, len(data)))
                                        ^^^^^^^^^
TypeError: object of type 'NoneType' has no len() 

因为get_chapter_content函数没有返回值，所以data是None，导致len(data)报错。可以修改get_chapter_content函数，
让它返回章节内容的长度，或者直接在函数内部打印章节内容的长度，而不是在外部处理。
"""