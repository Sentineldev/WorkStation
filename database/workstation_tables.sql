CREATE TABLE IF NOT EXISTS person(
person_id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(20) NOT NULL,
last_name VARCHAR(20) NOT NULL,
nationality VARCHAR(30) NOT NULL,
birthdate DATE NOT NULL
)

CREATE TABLE IF NOT EXISTS phone(
person_id INT NOT NULL REFERENCES person (person_id),
phone_number VARCHAR(15) PRIMARY KEY
)

CREATE TABLE IF NOT EXISTS user(
user_id INT AUTO_INCREMENT PRIMARY KEY,
person_id INT NOT NULL REFERENCES person (person_id),
username VARCHAR(20) NOT NULL,
password VARCHAR(16) NOT NULL
)