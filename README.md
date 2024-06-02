# 下載網站小說
> 此程式適用下載完結小說，下載的章節內容會統一存在同個txt檔

> 個人是將載好的txt檔案，匯到輕鬆讀小說APP的書櫃

> headers:\n'YourBotName/1.0 (yourmail@gmail.com)'\n'YourBotName/1.0 (+http://yourwebsite.com/contact)'\n'YourBotName/1.0 (+http://yourwebsite.com/contact) yourmail@gmail.com'

## 可樂小說網 [keleshuba.net](https://www.keleshuba.net/)
### 程式碼 [link](https://github.com/JhihHan/download_novel/blob/main/keleshuba_net.py)
> 導入特定函數、定義headers和cc
```python=
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
```
> 處理檔名和章節連結
```python=
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
```
> 下載章節內容
```python=
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
```
> 儲存檔案
```python=
def save_to_txt(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')
```
> 主函數
```python=
def main():
    base_url = ''
    novel_name, chapter_links = fetch_chapter_links(base_url)

    # 文件名使用小说名称
    filename = f'《{novel_name.strip().replace(" ", "_").replace("/", "_")}》.txt'

    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url)

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)

        # 设置随机延迟
        time.sleep(random.uniform(0.5, 1))

    print(f'\nDownload of 《{novel_name}》 completed!')

if __name__ == "__main__":
    main()
```
### 實際操作
> 1.至小說網站選擇要下載的小說



> 2.複製小說網址



> 3.將網址貼至base_url行''內 -> 4.開始執行 -> 5.下載進度 -> 6.下載結果



## 小說狂人 [czbooks.net](https://czbooks.net)
### 程式碼 [link](https://github.com/JhihHan/download_novel/blob/main/czbooks_net.py)
> 導入特定函數、定義headers
```python=
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

headers = {'User-Agent': 'YourBotName/1.0 (+http://yourwebsite.com/contact) yourmail@gmail.com'}
```
> 處理檔名和章節連結
```python=
def fetch_chapter_links(url):   
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    #小說名稱    
    novel_name = soup.find('span', class_='title').get_text(strip=True)

    #章節連結
    chapter_links = []
    chapter_list = soup.find('ul', class_='nav chapter-list', id='chapter-list')
    if chapter_list:
        for a_tag in chapter_list.find_all('a', href=True):
            chapter_url = urljoin(url, a_tag['href'])
            chapter_links.append(chapter_url)
    
    return novel_name, chapter_links
```
> 下載章節內容
```python=
def fetch_article_content(url):
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    #小說內容
    article_content_div = soup.find('div', class_='content')
    
    if not article_content_div:
        raise Exception("Failed to find the article content on the page")

    article_text = article_content_div.get_text('\n', strip=True)
    
    return article_text
```
> 儲存檔案
```python=
def save_to_txt(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
        file.write('\n\n')
```
> 主函數
```python=
def main():
    base_url = '' #小說網址
    novel_name, chapter_links = fetch_chapter_links(base_url)

    filename = novel_name.strip().replace(" ", "_").replace("/", "_")+'.txt'

    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
        article_text = fetch_article_content(chapter_url)
        
        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)

        save_to_txt(formatted_text, filename)
        time.sleep(random.uniform(0.5, 1))
    
    print(f'Download of {novel_name} completed!')

if __name__ == "__main__":
    main()
```
### 實際操作
> 1.至小說網站選擇要下載的小說

![image](https://github.com/JhihHan/download_novel/assets/117454279/486b2997-d7f8-4804-ab41-29ef2a256ba3)

> 2.複製小說網址

![image](https://github.com/JhihHan/download_novel/assets/117454279/d5507306-5aa8-4f6d-a043-aa2ad6fbb290)

> 3.將網址貼至base_url行''內 -> 4.開始執行 -> 5.下載進度 -> 6.下載結果

![image](https://github.com/JhihHan/download_novel/assets/117454279/7e72e3cc-4aef-455e-8360-3d053d08c683)
