# 🌦️ Weather Data Pipeline

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)

A containerized pipeline that fetches weather data from OpenWeatherMap API, stores it in MySQL, and displays it via a Flask web interface.

## 📌 Features

- ✅ Fetches temperature, description, and humidity forecasts
- ✅ Stores data in MySQL database
- ✅ Simple web interface to view data
- ✅ Fully containerized with Docker Compose

## 🏗 Project Structure
weather-data-pipeline/

├── app/

│ └── main.py # Flask application

├── docker-compose.yml # Service orchestration

├── Dockerfile # Flask container setup

├── script.sql # DB initialization

├── requirements.txt # Python dependencies

└── .env.example # Environment template


## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenWeatherMap API key

### 1. Clone the repository
```bash
git clone https://github.com/your-username/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Configure environment
   ```bash 
cp .env.example .env
# Edit .env with your API key

```
### 3. Start services
``` bash
docker compose up --build -d
```
### 4. Access the web interface
```bash
http://localhost:5000
```
## 🛠 Technologies Used

| Component          | Technology           | Badge |
|--------------------|----------------------|-------|
| Containerization   | Docker               | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) |
| Database           | MySQL 8              | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white) |
| Web Framework      | Flask                | ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white) |
| Programming Language | Python 3.9        | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) |
| API Client         | Requests             | ![Requests](https://img.shields.io/badge/Requests-3776AB?logo=python&logoColor=white) |
| Environment Management | python-dotenv   | ![Dotenv](https://img.shields.io/badge/python--dotenv-3776AB?logo=python&logoColor=white) |
## 💻 Code Snippets
Flask API Call
``` python
@app.route('/')
def display_weather():
    weather_data = get_weather_data()
    return render_template('index.html', data=weather_data)
```

MySQL Table Schema
``` sql
CREATE TABLE weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    datetime DATETIME,
    temperature FLOAT,
    description VARCHAR(100),
    humidity INT
);
```
## 🔍 How It Works


| # | Source          | Target            | Protocol | Data Format       | Description |
|---|-----------------|-------------------|----------|-------------------|-------------|
| 1 | User            | Flask App         | HTTP     | GET /             | Page request |
| 2 | Flask App       | OpenWeatherMap    | HTTPS    | JSON              | API key + city |
| 3 | OpenWeatherMap  | Flask App         | HTTPS    | JSON              | Temp, humidity, desc |
| 4 | Flask App       | MySQL             | TCP      | SQL               | INSERT weather_data |
| 5 | Flask App       | User              | HTTP     | HTML              | Rendered template |
## 🛑 Troubleshooting
MySQL Connection Issues:

``` bash
docker compose logs mysql

```
API Errors:
```bash
# Verify your API key is correct in .env
OPENWEATHER_API_KEY=your_api_key_here
```
