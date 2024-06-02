import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from opencc import OpenCC

headers = {'User-Agent': 'Download_the_novel_and_read_it_myself/1.0 (su395014um@gmail.com)'}
cc = OpenCC('s2twp')

def fetch_chapter_links(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到小说名称
    block_txt2_div = soup.find('div', class_='block_txt2')
    name = block_txt2_div.find('h2').get_text(strip=True)
    novel_name = cc.convert(name)

    # 找到所有章节链接
    chapter_links = []
    chapter_list = soup.find('ul', id='allChapters2', class_='chapter')
    if chapter_list:
        for a_tag in chapter_list.find_all('a', href=True):
            chapter_url = urljoin(url, a_tag['href'])
            chapter_links.append(chapter_url)

    return novel_name, chapter_links

def fetch_article_content(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    title_div = soup.find('div', id='nr_title')
    if title_div:
        title = title_div.get_text(strip=True)
        title_text = cc.convert(title)
    
    article_content_div = soup.find('div', id='nr1')
    if article_content_div:
        text = article_content_div.get_text('\n', strip=True)
        article_text = cc.convert(text)

    lines = article_text.split('\n')
    lines.insert(0, title_text)
    article_text_with_title = '\n'.join(lines)

    return article_text_with_title

def save_to_txt(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')

def main():
    base_url = 'https://www.keleshuba.net/book/231641/'
    novel_name, chapter_links = fetch_chapter_links(base_url)

    # 文件名使用小说名称
    filename = f'/content/drive/MyDrive/novel/《{novel_name.strip().replace(" ", "_").replace("/", "_")}》.txt'

    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url)

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)

        # 设置随机延迟
        time.sleep(random.uniform(0.5, 1))

    print(f'\nDownload of {novel_name} completed!')

if __name__ == "__main__":
    main()
