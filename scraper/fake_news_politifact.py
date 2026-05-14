import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_politifact_test():
    print("1. Starting PolitiFact (Fake News) Scraper...")
    # This specific URL only loads claims they have rated "False"
    base_url = "https://www.politifact.com/factchecks/list/?ruling=false"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(base_url, headers=headers)
        print(f"2. Connected to PolitiFact! (Status Code: {response.status_code})")
    except Exception as e:
        print(f"FAILED to connect: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # PolitiFact keeps their articles in 'li' tags with this specific class
    articles = soup.find_all('li', class_='o-listicle__item')
    print(f"3. Found {len(articles)} claims on the page.")
    
    data = []
    
    for article in articles[:5]:
        # Grab the quote/claim
        quote_div = article.find('div', class_='m-statement__quote')
        if not quote_div:
            continue
            
        headline = quote_div.get_text(strip=True)
        link_tag = quote_div.find('a')
        
        # PolitiFact uses relative URLs, so we have to add the domain name
        url = "https://www.politifact.com" + link_tag['href'] if link_tag else "No Link"
        
        print(f" -> Scraping Fake Claim: {headline[:40]}...")
        
        data.append({
            'Headline': headline,
            # For fake news claims, the headline/quote IS usually the full text we want to analyze
            'Article_Text': headline, 
            'Source_URL': url,
            'Label': 0  # 0 represents Fake News
        })
        time.sleep(1) 
            
    df = pd.DataFrame(data)
    df.to_csv('data/fake_news_test.csv', index=False)
    print(f"\n4. SUCCESS! Saved {len(data)} fake claims to data/fake_news_test.csv")

if __name__ == "__main__":
    scrape_politifact_test()