import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_guardian(target_count=1250):
    print(f"Starting The Guardian Scraper to collect {target_count} real news articles...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = []
    page = 1

    while len(data) < target_count:
        url = f"https://www.theguardian.com/world?page={page}"
        print(f"\n--- Scraping Page {page} (Currently have {len(data)} articles) ---")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Blocked or out of pages. Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            all_links = soup.find_all('a')
            unique_urls = []
            
            for link in all_links:
                href = link.get('href', '')
                
                # ---> THE FIX <---
                # If the link is relative (starts with /), add the domain name!
                if href.startswith('/'):
                    href = 'https://www.theguardian.com' + href
                    
                # Now our filter works perfectly
                if 'theguardian.com/world/20' in href and '/video/' not in href and '/audio/' not in href and '/live/' not in href:
                    unique_urls.append(href)
            
            unique_urls = list(set(unique_urls))
            
            if not unique_urls:
                print("No articles found on this page. Moving to next page...")
                page += 1
                time.sleep(1)
                continue

            for article_url in unique_urls:
                if len(data) >= target_count:
                    break
                    
                try:
                    article_res = requests.get(article_url, headers=headers, timeout=10)
                    article_soup = BeautifulSoup(article_res.text, 'html.parser')
                    
                    headline_tag = article_soup.find('h1')
                    if not headline_tag: 
                        continue
                    headline = headline_tag.get_text(strip=True)
                    
                    paragraphs = article_soup.find_all('p')
                    article_text = " ".join([p.get_text(strip=True) for p in paragraphs])
                    
                    if len(article_text) > 200:
                        data.append({
                            'Headline': headline,
                            'Article_Text': article_text,
                            'Source_URL': article_url,
                            'Label': 1 
                        })
                        print(f"  [SUCCESS] {len(data)}: {headline[:50]}...")
                    
                    time.sleep(1) 
                    
                except Exception:
                    print("  [SKIP] Failed to load article content.")
            
            page += 1
            
            if data:
                if not os.path.exists('data'):
                    os.makedirs('data')
                df = pd.DataFrame(data)
                df.to_csv('data/guardian_raw.csv', index=False)
                
        except Exception as e:
            print(f"Fatal Error on page {page}: {e}")
            break

if __name__ == "__main__":
    scrape_guardian(target_count=1250)