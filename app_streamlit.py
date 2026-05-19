import streamlit as st
import pickle
import re
import nltk
from nltk.corpus import stopwords

# Setup NLTK
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# UI Config
st.set_page_config(page_title="AI Fake News Detector", page_icon="📰")
st.title("📰 Fake News Detector")
st.write("Built with Logistic Regression and TF-IDF Vectorization")

# Load Brain
model = pickle.load(open('models/fake_news_model.pkl', 'rb'))
vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))

# Input area
user_input = st.text_area("Paste the article text here:", height=250)

if st.button("Analyze Authenticity"):
    if len(user_input) > 50:
        cleaned = clean_text(user_input)
        vec = vectorizer.transform([cleaned])
        prediction = model.predict(vec)[0]
        confidence = model.predict_proba(vec).max() * 100
        
        if prediction == 1:
            st.success(f"✅ VERDICT: REAL NEWS ({confidence:.2f}% Confidence)")
        else:
            st.error(f"🚨 VERDICT: FAKE NEWS ({confidence:.2f}% Confidence)")
    else:
        st.warning("Please paste at least 50 characters for a valid analysis.")