import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

# Extract features for ML
def extract_features(urls):
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
    features = vectorizer.fit_transform(urls)
    return features, vectorizer

# Train ML model
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

# Build domain graph
def build_domain_graph():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls")
    urls = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    G = nx.Graph()
    # Extract domains
    domains = [urlparse(url).netloc for url in urls]
    # Add nodes (domains)
    for domain in domains:
        G.add_node(domain)
    # Add edges (simplified: connect domains with similar suffixes)
    for i, d1 in enumerate(domains):
        for d2 in domains[i+1:]:
            if d1.split('.')[-1] == d2.split('.')[-1]:  # Same TLD (e.g., .com)
                G.add_edge(d1, d2)
    return G

# Get connected components (clusters)
def get_graph_clusters():
    G = build_domain_graph()
    clusters = list(nx.connected_components(G))
    return [{"cluster_id": i, "domains": list(cluster)} for i, cluster in enumerate(clusters)]

if __name__ == "__main__":
    model, vectorizer = train_model()
    clusters = get_graph_clusters()
    print("Model trained and graph clusters:", clusters)