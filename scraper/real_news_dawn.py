import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import os

def scrape_dawn(target_count=1200):
    print(f"Starting DAWN News Scraper to collect {target_count} articles...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    data = []
    
    # Start from today's date
    current_date = datetime.now()

    # This loop keeps running backward through time until we have enough articles
    while len(data) < target_count:
        # Format the date exactly how Dawn News expects it in the URL (YYYY-MM-DD)
        date_str = current_date.strftime("%Y-%m-%d")
        url = f"https://www.dawn.com/latest-news/{date_str}"
        
        print(f"\n--- Scraping Date: {date_str} (Currently have {len(data)} articles) ---")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Error or blocked on {date_str}. Status: {response.status_code}")
                # Even if one date fails, we subtract a day and keep going
                current_date -= timedelta(days=1)
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            
            if not articles:
                print(f"No articles found for {date_str}. Moving to previous day.")
            else:
                for article in articles:
                    if len(data) >= target_count:
                        break
                    
                    heading = article.find('h2')
                    if not heading: 
                        continue
                        
                    link_tag = heading.find('a')
                    if not link_tag: 
                        continue
                        
                    url_article = link_tag['href']
                    headline = heading.get_text(strip=True)
                    
                    # Visit the article to get the full text
                    try:
                        article_res = requests.get(url_article, headers=headers, timeout=10)
                        article_soup = BeautifulSoup(article_res.text, 'html.parser')
                        paragraphs = article_soup.find_all('p')
                        article_text = " ".join([p.get_text(strip=True) for p in paragraphs])
                        
                        # Only add if we actually got text (greater than 100 characters)
                        if len(article_text) > 100:
                            data.append({
                                'Headline': headline,
                                'Article_Text': article_text,
                                'Source_URL': url_article,
                                'Label': 1 
                            })
                            print(f"  [SUCCESS] {len(data)}: {headline[:50]}...")
                        
                        # Polite delay to prevent getting IP blocked
                        time.sleep(1) 
                        
                    except Exception:
                        print(f"  [SKIP] Failed to read article content for {headline[:20]}...")
            
            # After processing all articles for the day, go back exactly 1 day in time
            current_date -= timedelta(days=1)
            
        except Exception as e:
            print(f"Fatal Error on {date_str}: {e}")
            break

    # Save everything we found
    if data:
        # Check if data directory exists, if not, create it
        if not os.path.exists('data'):
            os.makedirs('data')
            
        df = pd.DataFrame(data)
        df.to_csv('data/dawn_raw.csv', index=False)
        print(f"\nFINISHED! Collected {len(data)} articles and saved to data/dawn_raw.csv")
    else:
        print("\nNo data collected. Something went wrong with the connection or tags.")

if __name__ == "__main__":
    scrape_dawn(target_count=1200)