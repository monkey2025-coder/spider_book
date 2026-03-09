# -*- encoding: utf-8 -*-
'''
file       :demo.py
Description:
Date       :2026/03/06 11:22:33
Author     :czy
version    :v0.01
email      :1060324818@qq.com
'''

import requests
from bs4 import BeautifulSoup
import re

pattern = r'^https://www\.erciyan\.com/book/\d+/\d+\.html$'

url_pattern = re.compile(pattern)

def check_url_format(url):
    if url_pattern.match(url):
        return True
    return False

if __name__ == '__main__':
    base_url = 'https://www.erciyan.com/book/94529913/'
    Chapters_base_url = "https://www.erciyan.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    Chapters = []
    
    for i in range(1, 1000000000):  
        url = f'{base_url}{i}/'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"正在获取目录：{url}")
        print(f"{response.status_code} {response.reason}")
        print(f"{response.text[:100]}...")

        for li in soup.find_all('li'):
            temp_url = li.find('a')['href']
            url = Chapters_base_url + temp_url
            if check_url_format(url):
                Chapters.append(url)

        if not "下一页" in response.text:
            break
    
    print(f"总目录已获取完成！{len(Chapters)}章")

    with open('Chapters.txt', 'w', encoding='utf-8') as f:
        for chapter in Chapters:
            f.write(chapter + '\n')