from flask import Flask, render_template_string
from dotenv import load_dotenv
import os
import requests
import mysql.connector
from datetime import datetime
import time
import subprocess

app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "weather_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "motdepasse_weather")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "weather_db")

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in .env file")

# Connexion à MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# Créer la table si elle n'existe pas
def ensure_table_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            date_time DATETIME NOT NULL,
            temperature FLOAT NOT NULL,
            description VARCHAR(255) NOT NULL,
            humidity INT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table weather_data vérifiée/créée avec succès.")

# Vider la table weather_data
def clear_weather_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE weather_data")
    conn.commit()
    cursor.close()
    conn.close()
    print("Table weather_data vidée avec succès.")

# Récupérer et stocker les données météo
def fetch_and_store_weather(city="Paris"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"Erreur lors de la récupération des données météo : {data.get('message', 'Erreur inconnue')}")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for forecast in data["list"]:
        date_time = datetime.fromtimestamp(forecast["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        temperature = forecast["main"]["temp"]
        description = forecast["weather"][0]["description"]
        humidity = forecast["main"]["humidity"]

        query = """
        INSERT INTO weather_data (city, date_time, temperature, description, humidity)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (city, date_time, temperature, description, humidity))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Données stockées pour 24 heures à {city}")

# Route principale pour afficher les données météo
@app.route('/')
def display_weather():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city, date_time, temperature, description, humidity FROM weather_data ORDER BY date_time")
    weather_data = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Données Météo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Données Météo pour Paris</h1>
        <table>
            <tr>
                <th>Ville</th>
                <th>Date et Heure</th>
                <th>Température (°C)</th>
                <th>Description</th>
                <th>Humidité (%)</th>
            </tr>
            {% for row in weather_data %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, weather_data=weather_data)

# Fonction principale
def main():
    ensure_table_exists()
    clear_weather_data()
    fetch_and_store_weather()

if __name__ == "__main__":
    # Attendre que MySQL soit prêt
    while subprocess.run(["nc", "-z", MYSQL_HOST, "3306"]).returncode != 0:
        time.sleep(1)

    # Lancer l'application
    main()
    app.run(host='0.0.0.0', port=5000)