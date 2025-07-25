from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os
import hashlib
import random
from graph_analysis import train_model, extract_features

app = Flask(__name__)
load_dotenv()

# Load ML model and vectorizer
model, vectorizer = train_model()

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

# Quantum-inspired random ID
def generate_quantum_id():
    return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()

@app.route('/check', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL required"}), 400
    # ML-based phishing check
    features = vectorizer.transform([url])
    is_phishing = bool(model.predict(features)[0])
    cursor = db.cursor()
    cursor.execute("INSERT INTO urls (url, is_phishing) VALUES (%s, %s)", (url, is_phishing))
    log_id = generate_quantum_id()
    cursor.execute(
        "INSERT INTO access_logs (id, ip_address, timestamp, endpoint) VALUES (%s, %s, NOW(), %s)",
        (log_id, request.remote_addr, '/check')
    )
    db.commit()
    cursor.close()
    return jsonify({"url": url, "is_phishing": is_phishing}), 200

@app.route('/urls', methods=['GET'])
def get_urls():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM urls")
    urls = cursor.fetchall()
    cursor.close()
    return jsonify(urls)

if __name__ == '__main__':
    app.run(debug=True)