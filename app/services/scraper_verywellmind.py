import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

BASE_URL = "https://www.verywellmind.com"
GUIDES_URL = f"{BASE_URL}/mental-health-4157281"
HEADERS = {"User-Agent": "Mozilla/5.0"}
A_Z_URL = "https://www.verywellmind.com/conditions-a-z-4797402"


def scrape_verywellmind_guides() -> List[Dict]:
    """
    Scrape topic guide titles and content from VerywellMind.
    Returns:
        List of dicts: {"text": ..., "metadata": {"source": ..., "title": ..., "type": "web"}}
    """
    results = []
    resp = requests.get(GUIDES_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    article_links = [
        a['href']
        for a in soup.find_all('a', href=True)
        if a['href'].startswith('https://www.verywellmind.com/')
    ]
    print(f"Extracted {len(article_links)} article links: {article_links}")
    for link in set(article_links):
        page = requests.get(link, headers=HEADERS)
        page_soup = BeautifulSoup(page.text, "html.parser")
        title = page_soup.find('h1').get_text(strip=True) if page_soup.find('h1') else link
        content_div = page_soup.find('div', class_='comp article-body-content')
        if content_div:
            print(f"Content found for {link}")
            text = content_div.get_text(separator='\n', strip=True)
            results.append({
                "text": text,
                "metadata": {
                    "source": link,
                    "title": title,
                    "type": "web"
                }
            })
        else:
            print(f"No content found for {link}")
    return results

def scrape_verywellmind_topics() -> List[Dict]:
    results = []
    # Step 1: Get all topic links from the A-Z page
    resp = requests.get(A_Z_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    topic_links = [
        a['href']
        for a in soup.find_all('a', href=True)
        if a['href'].startswith('https://www.verywellmind.com/') and '/-4797402' not in a['href']
    ]
    print(f"Found {len(topic_links)} topic links.")
    for link in set(topic_links):
        page = requests.get(link, headers=HEADERS)
        page_soup = BeautifulSoup(page.text, "html.parser")
        title = page_soup.find('h1').get_text(strip=True) if page_soup.find('h1') else link
        content_div = page_soup.find('div', class_='comp article-body-content')
        if content_div:
            text = content_div.get_text(separator='\n', strip=True)
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            for para in paragraphs:
                results.append({
                    "text": para,
                    "metadata": {
                        "source": link,
                        "title": title,
                        "type": "web"
                    }
                })
            print(f"Extracted {len(paragraphs)} paragraphs from {link}")
        else:
            print(f"No content found for {link}")
    return results

def scrape_verywellmind_section(section_url: str) -> List[Dict]:
    results = []
    resp = requests.get(section_url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Find all article links
    article_links = [
        a['href']
        for a in soup.find_all('a', href=True)
        if a['href'].startswith('https://www.verywellmind.com/')
    ]
    print(f"Extracted {len(article_links)} article links: {article_links}")
    for link in set(article_links):
        page = requests.get(link, headers=HEADERS)
        page_soup = BeautifulSoup(page.text, "html.parser")
        title = page_soup.find('h1').get_text(strip=True) if page_soup.find('h1') else link
        content_div = page_soup.find('div', class_='comp article-body-content')
        if content_div:
            print(f"Content found for {link}")
            text = content_div.get_text(separator='\n', strip=True)
            results.append({
                "text": text,
                "metadata": {
                    "source": link,
                    "title": title,
                    "type": "web"
                }
            })
        else:
            print(f"No content found for {link}")
    return results

def scrape_verywellmind_section_paginated(section_url: str, max_pages: int = 20) -> List[Dict]:
    results = []
    seen_links = set()
    page_num = 1
    while True:
        url = section_url
        if page_num > 1:
            if '?' in section_url:
                url = f"{section_url}&page={page_num}"
            else:
                url = f"{section_url}?page={page_num}"
        print(f"Scraping page {page_num}: {url}")
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Find all article links
        article_links = [
            a['href']
            for a in soup.find_all('a', href=True)
            if a['href'].startswith('https://www.verywellmind.com/')
        ]
        new_links = set(article_links) - seen_links
        print(f"Extracted {len(new_links)} new article links on page {page_num}")
        if not new_links:
            break
        for link in new_links:
            page = requests.get(link, headers=HEADERS)
            page_soup = BeautifulSoup(page.text, "html.parser")
            title = page_soup.find('h1').get_text(strip=True) if page_soup.find('h1') else link
            content_div = page_soup.find('div', class_='comp article-body-content')
            if content_div:
                print(f"Content found for {link}")
                text = content_div.get_text(separator='\n', strip=True)
                results.append({
                    "text": text,
                    "metadata": {
                        "source": link,
                        "title": title,
                        "type": "web"
                    }
                })
            else:
                print(f"No content found for {link}")
            time.sleep(0.5)  # Be polite to the server
        seen_links.update(new_links)
        # Check for a next page link (optional: can also just increment page_num)
        next_link = soup.find('a', attrs={'aria-label': 'Next'})
        if not next_link and len(new_links) == 0:
            break
        page_num += 1
        if page_num > max_pages:
            print("Reached max_pages limit.")
            break
    return results 