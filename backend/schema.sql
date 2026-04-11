-- schema.sql
-- Pet Adoption Website Schema
-- PostgreSQL
DROP TABLE IF EXISTS AdoptionApplication;
DROP TABLE IF EXISTS Pet;
DROP TABLE IF EXISTS UserTable;
CREATE TABLE UserTable (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE
);
CREATE TABLE Pet (
    pet_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    age INT NOT NULL CHECK (age >= 0),
    available BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE AdoptionApplication (
    application_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    pet_id INT NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (
        status IN ('Pending', 'Approved', 'Rejected', 'Withdrawn')
    ),
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES UserTable(user_id),
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id)
);
