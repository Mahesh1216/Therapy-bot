import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = "https://www.mind.org.uk"
SELF_HELP_URL = f"{BASE_URL}/information-support/types-of-mental-health-problems/"


def scrape_mind_org_uk_guides() -> List[Dict]:
    """
    Scrape worksheet/self-guide titles and content from Mind.org.uk.
    Returns:
        List of dicts: {"text": ..., "metadata": {"source": ..., "title": ..., "type": "web"}}
    """
    results = []
    resp = requests.get(SELF_HELP_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    guide_links = [a['href'] for a in soup.select('a') if a['href'].startswith('/information-support/types-of-mental-health-problems/')]
    for link in set(guide_links):
        url = BASE_URL + link
        page = requests.get(url)
        page_soup = BeautifulSoup(page.text, "html.parser")
        title = page_soup.find('h1').get_text(strip=True)
        content_div = page_soup.find('div', class_='rich-text')
        if content_div:
            text = content_div.get_text(separator='\n', strip=True)
            results.append({
                "text": text,
                "metadata": {
                    "source": url,
                    "title": title,
                    "type": "web"
                }
            })
    return results 