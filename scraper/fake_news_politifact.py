import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_politifact(target_count=1250):
    print(f"Starting PolitiFact Scraper to collect {target_count} fake news claims...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = []
    page = 1

    # Loop through PolitiFact pages until we hit our target
    while len(data) < target_count:
        url = f"https://www.politifact.com/factchecks/list/?page={page}&ruling=false"
        print(f"\n--- Scraping Page {page} (Currently have {len(data)} articles) ---")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Reached end of pages or blocked. Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # PolitiFact list items
            articles = soup.find_all('li', class_='o-listicle__item')
            
            if not articles:
                print("No more articles found.")
                break

            for article in articles:
                if len(data) >= target_count:
                    break
                    
                quote_div = article.find('div', class_='m-statement__quote')
                if not quote_div:
                    continue
                    
                headline = quote_div.get_text(strip=True)
                link_tag = quote_div.find('a')
                url_article = "https://www.politifact.com" + link_tag['href'] if link_tag else "No Link"
                
                # For PolitiFact, the claim itself acts as our fake news text
                data.append({
                    'Headline': headline,
                    'Article_Text': headline, 
                    'Source_URL': url_article,
                    'Label': 0 
                })
                print(f"  [SUCCESS] {len(data)}: {headline[:50]}...")
                
            # Move to next page and pause
            page += 1
            time.sleep(1) 
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    # Save to CSV
    if data:
        if not os.path.exists('data'):
            os.makedirs('data')
        df = pd.DataFrame(data)
        df.to_csv('data/politifact_raw.csv', index=False)
        print(f"\nFINISHED! Collected {len(data)} fake claims and saved to data/politifact_raw.csv")
    else:
        print("No data collected.")

if __name__ == "__main__":
    scrape_politifact(target_count=1250)