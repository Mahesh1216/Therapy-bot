from pathlib import Path
import sys
import re

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.core.config import Settings
from app.services.rag_service import RAGService
from app.services.scraper_therapistaid import scrape_therapistaid_worksheets
from app.services.scraper_verywellmind import scrape_verywellmind_section, scrape_verywellmind_topics
from app.services.scraper_mind_org_uk import scrape_mind_org_uk_guides
from app.services.scraper_nhs import scrape_nhs_guides
import requests
from bs4 import BeautifulSoup

SITES_FILE = Path(project_root) / "sitesURL.txt"

# Helper: extract all links from a hub page for a given domain
DOMAIN_SCRAPE_CONFIG = {
    "therapistaid.com": {
        "subtopic_selector": "a[href^='/worksheet/'], a[href^='/activity/'], a[href^='/tool/'], a[href^='/audio-resource/']",
        "base_url": "https://www.therapistaid.com"
    },
    "mind.org.uk": {
        "subtopic_selector": "a[href^='/information-support/types-of-mental-health-problems/']",
        "base_url": "https://www.mind.org.uk"
    },
    "nhs.uk": {
        "subtopic_selector": "a[href^='/mental-health/']",
        "base_url": "https://www.nhs.uk"
    },
}

def extract_links_from_hub(url: str, domain: str) -> list:
    config = DOMAIN_SCRAPE_CONFIG.get(domain)
    if not config:
        print(f"No config for domain: {domain}")
        return []
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = [a['href'] for a in soup.select(config['subtopic_selector']) if a.get('href')]
        # Make full URLs
        full_links = []
        for link in links:
            if link.startswith('http'):
                full_links.append(link)
            else:
                full_links.append(config['base_url'] + link)
        return list(set(full_links))
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return []

def get_domain(url: str) -> str:
    match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return match.group(1) if match else ""

def scrape_article(url: str) -> list:
    domain = get_domain(url)
    if "therapistaid.com" in domain:
        from app.services.scraper_therapistaid import scrape_therapistaid_worksheets
        return generic_scrape(url, domain)
    elif "verywellmind.com" in domain:
        print(f"Using section scraper for Verywell Mind: {url}")
        return scrape_verywellmind_section(url)
    elif "mind.org.uk" in domain:
        return generic_scrape(url, domain)
    elif "nhs.uk" in domain:
        return generic_scrape(url, domain)
    else:
        print(f"No scraper for domain: {domain}")
        return []

def generic_scrape(url: str, domain: str) -> list:
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else url
        if "therapistaid.com" in domain:
            content_div = soup.find('div', class_='worksheet-content')
        elif "verywellmind.com" in domain:
            content_div = soup.find('div', class_='comp article-body-content')
        elif "mind.org.uk" in domain:
            content_div = soup.find('div', class_='rich-text')
        elif "nhs.uk" in domain:
            content_div = soup.find('div', class_='nhsuk-u-reading-width')
        else:
            content_div = soup.find('body')
        if content_div:
            text = content_div.get_text(separator='\n', strip=True)
            return [{
                "text": text,
                "metadata": {
                    "source": url,
                    "title": title,
                    "type": "web"
                }
            }]
        else:
            print(f"No content found for {url}")
            return []
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def main():
    settings = Settings()
    rag_service = RAGService(settings)
    all_chunks = []

    # Read URLs from sitesURL.txt
    with open(SITES_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for line in lines:
        url = line.split('(')[0].strip()
        is_hub = '(All sub' in line or '(all Sub' in line or '(all sub' in line
        domain = get_domain(url)
        # Special handling for Verywell Mind A-Z topics page
        if url == "https://www.verywellmind.com/conditions-a-z-4797402":
            print(f"Using A-Z topics scraper for Verywell Mind: {url}")
            all_chunks.extend(scrape_verywellmind_topics())
            continue
        if is_hub:
            print(f"Crawling hub page: {url}")
            if "verywellmind.com" in domain:
                print(f"Using section scraper for Verywell Mind hub: {url}")
                all_chunks.extend(scrape_verywellmind_section(url))
            else:
                links = extract_links_from_hub(url, domain)
                print(f"  Found {len(links)} subtopic/article links.")
                for link in links:
                    all_chunks.extend(scrape_article(link))
        else:
            print(f"Scraping direct article: {url}")
            if "verywellmind.com" in domain:
                all_chunks.extend(scrape_verywellmind_section(url))
            else:
                all_chunks.extend(scrape_article(url))

    print(f"Total web documents to ingest: {len(all_chunks)}")
    if not all_chunks:
        print("No web documents found!")
        return

    print("Embedding and storing in Pinecone...")
    rag_service.embed_and_store(all_chunks)
    print("Done! Web knowledge base is ready.")

if __name__ == "__main__":
    main() 