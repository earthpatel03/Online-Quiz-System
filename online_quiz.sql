
CREATE DATABASE  quiz_app;
USE quiz_app;

-- 👤 USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100)
);

-- ❓ QUESTIONS TABLE (WITH TOPIC)
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    option1 VARCHAR(100),
    option2 VARCHAR(100),
    option3 VARCHAR(100),
    option4 VARCHAR(100),
    correct_answer VARCHAR(100),
    topic VARCHAR(50)
);

-- 📊 RESULTS TABLE
CREATE TABLE  resultss (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    score INT,
    topic VARCHAR(50),
    played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

select * from users;

select * from questions;

select * from results;

DROP TABLE results;

CREATE TABLE results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    score INT,
    topic VARCHAR(50),
    played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);