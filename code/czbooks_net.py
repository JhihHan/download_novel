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

headers = {'User-Agent': 'YourBotName/1.0 (+http://yourwebsite.com/contact) yourmail@gmail.com'}

def fetch_chapter_links(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到小说名称
    novel_name = soup.find('span', class_='title').get_text(strip=True)

    # 找到所有章节链接
    chapter_links = []
    chapter_title = []
    chapter_list = soup.find('ul', class_='nav chapter-list', id='chapter-list')
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
    article_content_div = soup.find('div', class_='content')

    if not article_content_div:
        raise Exception("Failed to find the article content on the page")

    article_text = article_content_div.get_text('\n', strip=True)
    article_text = f"{title}\n{article_text}"
    
    return article_text

def save_to_txt(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')

def main():
    base_url = ''
    novel_name, chapter_links, chapter_title = fetch_chapter_links(base_url)

    # 文件名使用小说名称
    filename = novel_name.strip().replace(" ", "_").replace("/", "_")+' .txt'

    i = 0
    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url, chapter_title[i])

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)
        i += 1
        # 设置随机延迟
        time.sleep(random.uniform(0.5, 1))

    print(f'\nDownload of {novel_name} completed!')

if __name__ == "__main__":
      main()
