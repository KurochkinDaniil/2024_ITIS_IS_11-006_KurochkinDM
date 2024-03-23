import sys
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_domain_from_url(url: str) -> str:
    if "://" in url:
        return url.split('/')[0] + '//' + url.split('/')[2]
    else:
        return url.split("/")[0]


def clean_space(text: str) -> str:
    paragraphs = text.split('\n')
    cleaned_paragraphs = [' '.join(paragraph.strip().split()) for paragraph in paragraphs if paragraph.strip()]
    cleaned_text = '\n'.join(cleaned_paragraphs)
    return cleaned_text


def download_page(url: str) -> (str | None, Exception | None):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text, None
        return None, Exception(f"Ошибка при скачивании {url}")
    except Exception as e:
        return None, e


def extract_links_and_text(html: str, domain: str) -> ([str], str):
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            href = urljoin(domain, href)
            links.append(href)

    for script_or_style in soup(["script", "style", "head", "title", "meta", "[document]"]):
        script_or_style.decompose()

    for block in soup.find_all(['p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        block.replace_with('\n' + block.text + '\n')

    text = clean_space(soup.get_text())

    return links, text


if __name__ == "__main__":
    urls = sys.argv[1:]
    downloaded_pages = 0
    i = 0
    open('index.txt', 'w', encoding='utf-8').close()
    seen_urls = set()

    while i < len(urls) and downloaded_pages < 100:
        if urls[i] in seen_urls:
            i += 1
            continue
        seen_urls.add(urls[i])

        html_content, err = download_page(urls[i])
        if err is not None:
            print(err)
            i += 1
            continue

        domain_ = get_domain_from_url(urls[i])
        if not html_content:
            print(f"Не удалось загрузить страницу: {urls[i]}")
            i += 1
            continue

        links_, text_ = extract_links_and_text(html_content, domain_)
        urls.extend(links_)

        words = re.findall(r'\w+', text_)
        if len(words) < 1000:
            print(f"На странице {urls[i]} не хватает слов.")
            i += 1
            continue

        filename = f"data/{downloaded_pages + 1}_page.txt"
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(text_)

        with open('index.txt', 'a', encoding='utf-8') as index_file:
            index_file.write(f"{downloaded_pages + 1}). {urls[i]}\n")
        downloaded_pages += 1

        print(f"Загружена {downloaded_pages} страница {urls[i]}")
        i += 1
