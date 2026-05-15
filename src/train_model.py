import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

def train_fake_news_model():
    print("1. Loading Cleaned Dataset...")
    try:
        df = pd.read_csv('data/cleaned_dataset.csv')
    except FileNotFoundError:
        print("Error: cleaned_dataset.csv not found. Did you run data_cleaning.py?")
        return

    # Sometimes cleaning removes all words (if an article was just links/numbers)
    # We drop any rows that became completely empty
    df = df.dropna(subset=['Clean_Text'])

    X = df['Clean_Text'] # The input (the article text)
    y = df['Label']      # The answer key (1 = Real, 0 = Fake)

    print(f"   Total valid articles for training: {len(df)}")

    print("\n2. Splitting data into Training (80%) and Testing (20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("\n3. Converting words to numbers (TF-IDF Vectorization)...")
    # We only look at the top 10,000 most important words to keep the model fast and efficient
    vectorizer = TfidfVectorizer(max_features=10000)
    
    # The vectorizer LEARNS the vocabulary from the training data, then transforms it
    X_train_vectorized = vectorizer.fit_transform(X_train)
    # The test data is ONLY transformed (no peeking at the answers!)
    X_test_vectorized = vectorizer.transform(X_test)

    print("\n4. Training the Logistic Regression AI Model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vectorized, y_train)

    print("\n5. Taking the Final Exam (Evaluating the Model)...")
    predictions = model.predict(X_test_vectorized)
    
    acc = accuracy_score(y_test, predictions)
    print(f"\n✅ FINAL EXAM SCORE (ACCURACY): {acc * 100:.2f}%\n")
    
    print("--- Detailed Classification Report ---")
    print(classification_report(y_test, predictions, target_names=['Fake News (0)', 'Real News (1)']))

    print("\n6. Saving the 'Brain' to disk...")
    # Create a new folder for your saved models
    if not os.path.exists('models'):
        os.makedirs('models')
        
    # We must save BOTH the model and the vectorizer
    with open('models/fake_news_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
        
    with open('models/tfidf_vectorizer.pkl', 'wb') as vec_file:
        pickle.dump(vectorizer, vec_file)
        
    print("SUCCESS! Model and Vectorizer safely saved in the /models directory.")

if __name__ == "__main__":
    train_fake_news_model()