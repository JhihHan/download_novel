import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

headers = {'User-Agent': 'YourBotName/1.0 (+http://yourwebsite.com/contact) yourmail@gmail.com'}
base_url = ''

def fetch_chapter_links(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到小说名称
    novel_name = soup.find('div', class_='book-describe').find('h1').text.strip()

    # 找到所有章节链接
    chapter_links = []
    chapter_title = []
    chapter_list = soup.find('div', class_='book-list clearfix')
    if chapter_list:
        for a_tag in chapter_list.find_all('a', href=True):
            chapter_title.append(a_tag.get_text(strip=True))
            chapter_url = urljoin(url, a_tag['href'])
            chapter_links.append(chapter_url)

    return novel_name, chapter_links, chapter_title

def fetch_article_content(url, title):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', id='nr1')
        
    if content_div:
        content = content_div.get_text(separator='\n', strip=True)
        content_lines = content.split('\n')
        article_content = '\n'.join(content_lines[:-1])
        article_text = f"{title}\n{article_content}"

    return article_text

def save_to_txt(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')

def main():
    novel_name, chapter_links, chapter_title = fetch_chapter_links(base_url)

    # 文件名使用小说名称
    filename = f'/content/drive/MyDrive/novel/《{novel_name.strip().replace(" ", "_").replace("/", "_")}》.txt'
    i = 0
    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url, chapter_title[i])

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)
        i += 1
        # 设置随机延迟
        time.sleep(random.uniform(0.5, 1))

    print(f'\nDownload of 《{novel_name}》 completed!')

if __name__ == "__main__":
    main()
