import pickle
import re
import nltk
from nltk.corpus import stopwords

# 1. We need the exact same cleaning function so the AI reads the text the same way
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def test_article():
    print("Loading AI Brain...")
    # 2. Load your saved models
    try:
        with open('models/fake_news_model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('models/tfidf_vectorizer.pkl', 'rb') as vec_file:
            vectorizer = pickle.load(vec_file)
    except FileNotFoundError:
        print("Error: Could not find the saved models in the /models folder.")
        return

    print("\n" + "="*50)
    print("📰 FAKE NEWS DETECTOR ACTIVATED")
    print("="*50)
    
    # 3. Create a loop to test articles
    while True:
        print("\nPaste the text of an article below (or type 'quit' to exit):")
        user_input = input("> ")
        
        if user_input.lower() == 'quit':
            break
            
        if len(user_input) < 20:
            print("Please paste a longer piece of text for an accurate prediction.")
            continue
            
        # 4. Clean, Vectorize, and Predict
        cleaned_input = clean_text(user_input)
        vectorized_input = vectorizer.transform([cleaned_input])
        
        prediction = model.predict(vectorized_input)[0]
        confidence = model.predict_proba(vectorized_input).max() * 100
        
        print("\n" + "-"*30)
        if prediction == 1:
            print(f"🟢 VERDICT: REAL NEWS (Confidence: {confidence:.2f}%)")
        else:
            print(f"🔴 VERDICT: FAKE NEWS (Confidence: {confidence:.2f}%)")
        print("-"*30)

if __name__ == "__main__":
    test_article()