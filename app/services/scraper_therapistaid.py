import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = "https://www.therapistaid.com"
WORKSHEETS_URL = f"{BASE_URL}/therapy-worksheets"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def scrape_therapistaid_worksheets() -> List[Dict]:
    """
    Scrape worksheet titles and content from TherapistAid.
    Returns:
        List of dicts: {"text": ..., "metadata": {"source": ..., "title": ..., "type": "web"}}
    """
    results = []
    resp = requests.get(WORKSHEETS_URL, headers=HEADERS)
    print("--- HTML received from server (first 2000 chars) ---")
    print(resp.text[:2000])
    print("--- END HTML ---")
    soup = BeautifulSoup(resp.text, "html.parser")
    # Find all anchor tags that link to worksheet detail pages
    worksheet_links = [
        a['href']
        for a in soup.find_all('a', href=True)
        if a['href'].startswith('/worksheet/')
    ]
    print(f"Extracted {len(worksheet_links)} worksheet links: {worksheet_links}")
    for link in set(worksheet_links):
        url = BASE_URL + link
        page = requests.get(url, headers=HEADERS)
        page_soup = BeautifulSoup(page.text, "html.parser")
        title = page_soup.find('h1').get_text(strip=True) if page_soup.find('h1') else url
        content_div = page_soup.find('div', class_='worksheet-content')
        if content_div:
            print(f"Content found for {url}")
            text = content_div.get_text(separator='\n', strip=True)
            results.append({
                "text": text,
                "metadata": {
                    "source": url,
                    "title": title,
                    "type": "web"
                }
            })
        else:
            print(f"No content found for {url}")
    return results 