import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_dawn_test():
    print("1. Starting DAWN News Scraper...")
    base_url = "https://www.dawn.com/latest-news"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(base_url, headers=headers)
        print(f"2. Connected to Dawn News! (Status Code: {response.status_code})")
    except Exception as e:
        print(f"FAILED to connect to internet: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Let's see exactly how many tags it finds
    articles = soup.find_all('article')
    print(f"3. Found {len(articles)} <article> tags on the page.")
    
    if len(articles) == 0:
        print("ERROR: Found 0 articles! Dawn News probably changed their website layout. We need to inspect their HTML.")
        return

    data = []
    
    for article in articles[:5]:
        heading = article.find('h2')
        if not heading:
            continue
            
        link_tag = heading.find('a')
        if not link_tag:
            continue
            
        url = link_tag['href']
        headline = heading.get_text(strip=True)
        
        print(f" -> Scraping: {headline[:40]}...")
        
        try:
            article_res = requests.get(url, headers=headers)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')
            paragraphs = article_soup.find_all('p')
            article_text = " ".join([p.get_text(strip=True) for p in paragraphs])
            
            data.append({
                'Headline': headline,
                'Article_Text': article_text,
                'Source_URL': url,
                'Label': 1 
            })
            time.sleep(1) 
            
        except Exception as e:
            print(f"    Failed to scrape text. Error: {e}")
            
    # Check if the data folder actually exists where we are running the script
    if not os.path.exists('data'):
        print("\nERROR: I cannot find the 'data' folder! Make sure you run this script from the main 'ai-fake-news-scraper' folder.")
        return

    df = pd.DataFrame(data)
    df.to_csv('data/real_news_test.csv', index=False)
    print(f"\n4. SUCCESS! Saved {len(data)} articles to data/real_news_test.csv")

if __name__ == "__main__":
    scrape_dawn_test()