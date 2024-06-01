import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

def fetch_chapter_links(url):
    headers = {'User-Agent': 'YourBotName/1.0 (+http://yourwebsite.com/contact)'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到小说名称
    novel_name = soup.find('span', class_='title').get_text(strip=True)

    # 找到所有章节链接
    chapter_links = []
    chapter_list = soup.find('ul', class_='nav chapter-list', id='chapter-list')
    if chapter_list:
        for a_tag in chapter_list.find_all('a', href=True):
            chapter_url = urljoin(url, a_tag['href'])
            chapter_links.append(chapter_url)

    return novel_name, chapter_links

def fetch_article_content(url):
    headers = {'User-Agent': 'YourBotName/1.0 (+http://yourwebsite.com/contact)'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    article_content_div = soup.find('div', class_='content')

    if not article_content_div:
        raise Exception("Failed to find the article content on the page")

    article_text = article_content_div.get_text('\n', strip=True)

    return article_text

def save_to_txt(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')

def main():
    base_url = 'https://czbooks.net/n/s6gd5e66'
    novel_name, chapter_links = fetch_chapter_links(base_url)

    # 文件名使用小说名称
    filename = f'/content/drive/MyDrive/novel/{novel_name.strip().replace(" ", "_").replace("/", "_")}.txt'

    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url)

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)

        # 设置随机延迟
        time.sleep(random.uniform(1, 3))

    print(f'\nDownload of {novel_name} completed!')

if __name__ == "__main__":
    # 免责声明
    print("免责声明：此代码仅供教育和研究用途。请勿用于任何违反法律或网站使用条款的行为。用户应确保其行为合法并遵守相关条款。")
    main()
