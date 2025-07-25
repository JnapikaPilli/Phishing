# 🛡️ Phishing Detection System

A cybersecurity project to detect phishing URLs using machine learning, graph analysis, and secure logging. Built with **Python**, **Flask**, **MySQL**, **scikit-learn**, and **NetworkX**, this project showcases skills in programming, data structures, algorithms, and RESTful API development.

---

## 🚀 Features

- **Phishing Detection**: Logistic Regression classifier to identify phishing URLs.
- **Graph Analysis**: Uses `NetworkX` to find relationships between domains.
- **Secure Logging**: Logs all API interactions with unique SHA-256 IDs.
- **REST API**:
  - `POST /check`: Check if a URL is phishing.
  - `GET /urls`: View all classified URLs.
  - `GET /graph`: Retrieve domain graph relationships.

---

## 🧰 Technologies Used

- **Python**: Core development language.
- **Flask**: Lightweight web framework for API endpoints.
- **MySQL**: Database to store classified URLs and logs.
- **scikit-learn**: Machine learning library for phishing detection.
- **NetworkX**: Graph-based domain analysis.
- **SHA-256**: Secure hash generation for log identifiers.

---

## ⚙️ Setup Instructions

##**1. Clone the Repository**##
git clone https://github.com/JnapikaPilli/Phishing.git
cd Phishing

##**2. Set Up Virtual Environment**##
python3 -m venv phishing_env
source phishing_env/bin/activate
pip install flask scikit-learn networkx mysql-connector-python python-dotenv
##**3. Install & Configure MySQL**##
Install MySQL:
sudo apt install mysql-server
Create Database and Tables:
CREATE DATABASE phishing_detector;
USE phishing_detector;
CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    is_phishing BOOLEAN
);
CREATE TABLE access_logs (
    id VARCHAR(64) PRIMARY KEY,
    ip_address VARCHAR(45),
    timestamp DATETIME,
    endpoint VARCHAR(100)
);
##**4. Set Environment Variables**##
Create a .env file in the project root:
nano .env
Add the following:
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_DATABASE=phishing_detector
##**5. Run the Application**##
python3 app.py
🔬 API Usage
Check a URL
curl -X POST -H "Content-Type: application/json" \
-d '{"url":"http://phishy.net"}' \
http://127.0.0.1:5000/check
*View All URLs*
curl http://127.0.0.1:5000/urls
Get Domain Graph
curl http://127.0.0.1:5000/graph
##**🌱 Future Improvements**##
Add more URL features (e.g., HTTPS usage, domain age).
Use edge weights in graph analysis for better accuracy.
Deploy to cloud platforms like AWS or Render.
Add unit testing and API authentication.
##**👤 Author**##
Jnapika Pilli

##**📄 License**##
This project is licensed under the MIT License.

##**📬 Contact**##
For questions or contributions, feel free to open an issue or submit a pull request.
