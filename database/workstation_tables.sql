CREATE TABLE IF NOT EXISTS person(
person_id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(20) NOT NULL,
last_name VARCHAR(20) NOT NULL,
country VARCHAR(30) NOT NULL,
birthdate DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS phone(
phone_number VARCHAR(15) PRIMARY KEY,
person_id INT REFERENCES person (person_id)
);

CREATE TABLE IF NOT EXISTS user(
user_id INT AUTO_INCREMENT PRIMARY KEY,
person_id INT REFERENCES person (person_id),
username VARCHAR(20) NOT NULL,
password VARCHAR(16) NOT NULL
);