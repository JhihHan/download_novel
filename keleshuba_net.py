"""
免责声明：

此爬虫代码仅用于个人学习和研究目的。通过使用该代码，您明确同意以下事项：

1. 此代码仅用于收集和下载网站上公开可访问的小说内容，以供个人阅读和研究。您应该遵守所访问网站的使用条款和版权法律。

2. 您应该在使用此代码时自行承担责任，包括但不限于对您所下载内容的合法性和准确性负责。我们对您可能因使用此代码而产生的任何后果概不负责。

3. 我们不保证此代码的适用性、准确性、可靠性、完整性或及时性。我们不对您因使用或无法使用此代码而造成的任何直接或间接损失或损害承担责任。

4. 我们保留随时更改此免责声明的权利。您应定期查看此页面以获取最新的免责声明。

通过使用此代码，您表明您已阅读、理解并同意此免责声明的所有条款和条件。如果您不同意这些条款，请勿使用此代码。
"""
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from opencc import OpenCC  #pip install opencc-python-reimplemented

headers = {'User-Agent': 'Download_the_novel_and_read_it_myself/1.0 (su395014um@gmail.com)'}
cc = OpenCC('s2twp') #簡轉繁 | 't2s'為繁轉簡

def fetch_chapter_links(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 小说名称
    block_txt2_div = soup.find('div', class_='block_txt2')
    name = block_txt2_div.find('h2').get_text(strip=True)
    novel_name = cc.convert(name)

    # 所有章节链接
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
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')

def main():
    base_url = ''
    novel_name, chapter_links = fetch_chapter_links(base_url)

    filename = f'《{novel_name.strip().replace(" ", "_").replace("/", "_")}》.txt'

    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url)

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)

        time.sleep(random.uniform(0.5, 1))

    print(f'\nDownload of 《{novel_name}》 completed!')

if __name__ == "__main__":
    main()
