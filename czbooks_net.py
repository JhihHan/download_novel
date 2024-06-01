import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

def fetch_chapter_links(url):
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    novel_name = soup.find('span', class_='title').get_text(strip=True)

    chapter_links = []
    chapter_list = soup.find('ul', class_='nav chapter-list', id='chapter-list')
    if chapter_list:
        for a_tag in chapter_list.find_all('a', href=True):
            chapter_url = urljoin(url, a_tag['href'])
            chapter_links.append(chapter_url)
    
    return novel_name, chapter_links

def fetch_article_content(url):
    response = requests.get(url)
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
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    base_url = ''
    novel_name, chapter_links = fetch_chapter_links(base_url)

    all_content = []

    for chapter_url in tqdm(chapter_links, desc="Downloading chapters"):
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
