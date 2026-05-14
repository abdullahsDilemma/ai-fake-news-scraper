import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_factcheck(target_count=1250):
    print(f"Starting FactCheck.org Scraper to collect {target_count} fake news claims...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = []
    page = 1

    while len(data) < target_count:
        # FactCheck.org pagination is very stable
        url = f"https://www.factcheck.org/page/{page}/"
        print(f"\n--- Scraping Page {page} (Currently have {len(data)} articles) ---")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Blocked or out of pages. Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all article blocks on the page
            articles = soup.find_all('article')
            
            if not articles:
                print("No articles found on this page.")
                break

            for article in articles:
                if len(data) >= target_count:
                    break
                    
                # The headline usually contains the false claim they are debunking
                heading = article.find('h3', class_='entry-title')
                if not heading: 
                    continue
                    
                link_tag = heading.find('a')
                if not link_tag: 
                    continue
                    
                article_url = link_tag['href']
                headline = heading.get_text(strip=True)
                
                try:
                    # Visit the article to get the text
                    article_res = requests.get(article_url, headers=headers, timeout=10)
                    article_soup = BeautifulSoup(article_res.text, 'html.parser')
                    
                    # We grab the first few paragraphs where they explain the viral fake claim
                    content_div = article_soup.find('div', class_='entry-content')
                    if content_div:
                        paragraphs = content_div.find_all('p')
                        # Combine first 3 paragraphs to get the context of the fake rumor
                        article_text = " ".join([p.get_text(strip=True) for p in paragraphs[:3]])
                        
                        if len(article_text) > 100:
                            data.append({
                                'Headline': headline,
                                'Article_Text': article_text,
                                'Source_URL': article_url,
                                'Label': 0 # 0 for Fake News
                            })
                            print(f"  [SUCCESS] {len(data)}: {headline[:50]}...")
                    
                    time.sleep(1) 
                    
                except Exception:
                    print("  [SKIP] Failed to load article content.")
            
            page += 1
            
            # --- AUTO SAVE ---
            if data:
                if not os.path.exists('data'):
                    os.makedirs('data')
                df = pd.DataFrame(data)
                df.to_csv('data/factcheck_raw.csv', index=False)
                
        except Exception as e:
            print(f"Fatal Error on page {page}: {e}")
            break

if __name__ == "__main__":
    scrape_factcheck(target_count=1250)