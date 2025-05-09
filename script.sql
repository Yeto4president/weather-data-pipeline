CREATE DATABASE IF NOT EXISTS weather_db;
USE weather_db;

CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    date_time DATETIME NOT NULL,
    temperature FLOAT NOT NULL,
    description VARCHAR(255) NOT NULL,
    humidity INT NOT NULL
);

CREATE DATABASE IF NOT EXISTS airflow;