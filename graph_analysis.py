import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def extract_features(urls):
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
    features = vectorizer.fit_transform(urls)
    return features, vectorizer

def train_model():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url, is_phishing FROM urls")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    urls, labels = zip(*data)
    features, vectorizer = extract_features(urls)
    model = LogisticRegression()
    model.fit(features, labels)
    return model, vectorizer

if __name__ == "__main__":
    model, vectorizer = train_model()
    print("Model trained successfully!")