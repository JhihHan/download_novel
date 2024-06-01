# 下載網站小說
個人是將載好的txt檔案，匯到輕鬆讀小說APP的書櫃
## 小說狂人 czbooks.net
### 程式碼 czbooks_net.py
導入特定函數
```python=
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
```
處理檔名和章節連結
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
下載章節內容
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
儲存檔案
```python=
def save_to_txt(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
```
主函數
```python=
def main():
    base_url = '' #小說網址
    novel_name, chapter_links = fetch_chapter_links(base_url)

    all_content = []

    for chapter_url in chapter_links:
        article_text = fetch_article_content(chapter_url)

        lines = article_text.split('\n')
        formatted_text = '\n\n'.join(lines)
        all_content.append(formatted_text)

        time.sleep(1)
    
    full_text = '\n\n'.join(all_content)
    
    filename = novel_name.strip().replace(' ', '_').replace('/', '_') + '.txt'

    save_to_txt(full_text, filename)
    print(f'Saved novel to {filename}')

if __name__ == "__main__":
    main()
```
### 實際操作
1.至小說網站選擇要下載的小說

![image](https://github.com/JhihHan/download_novel/assets/117454279/486b2997-d7f8-4804-ab41-29ef2a256ba3)

2.複製小說網址

![image](https://github.com/JhihHan/download_novel/assets/117454279/d5507306-5aa8-4f6d-a043-aa2ad6fbb290)

3.將網址貼至base_url行''內 -> 4.開始執行 -> 5.下載進度 -> 6.下載結果

![image](https://github.com/JhihHan/download_novel/assets/117454279/7e72e3cc-4aef-455e-8360-3d053d08c683)
