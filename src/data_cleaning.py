import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import os

def setup_nltk():
    print("Downloading NLTK stopwords...")
    # This quietly downloads the dictionary of English filler words
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

def clean_text(text):
    # 1. Convert to lowercase string
    text = str(text).lower()
    
    # 2. Remove all punctuation, special characters, and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 3. Remove common stop words ("the", "is", "in", etc.)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)

def process_data():
    setup_nltk()
    
    print("\nLoading Master Dataset...")
    df = pd.read_csv('data/master_dataset.csv')
    
    print(f"Cleaning {len(df)} articles... (This might take 1-2 minutes)")
    # Apply our cleaning function to every single row in the Article_Text column
    df['Clean_Text'] = df['Article_Text'].apply(clean_text)
    
    print("Saving cleaned dataset...")
    df.to_csv('data/cleaned_dataset.csv', index=False)
    
    print("\n✅ SUCCESS! Text preprocessing complete.")
    print("Here is a sneak peek of the clean text:")
    print(df[['Article_Text', 'Clean_Text']].head(2))

if __name__ == "__main__":
    process_data()