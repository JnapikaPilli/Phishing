from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os
import hashlib
import random

app = Flask(__name__)
load_dotenv()

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
    # Placeholder phishing check (to be enhanced with ML)
    is_phishing = len(url) < 10  # Simple rule for MVP
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