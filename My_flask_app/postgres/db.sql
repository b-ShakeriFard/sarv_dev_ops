-- Creating a table with the title "data store"
CREATE DATABASE postgresdb;

-- connect
\c postgresdb;

-- create table
CREATE TABLE users (
	id SERIAL PRIMARY KEY, 
	key TEXT NOT NULL,
	value TEXT NOT NULL
);


-- Insert three key-value pairs
INSERT INTO users (key, value) VALUES ('name', 'Behroox');
INSERT INTO users (key, value) VALUES ('city', 'Tehran');
INSERT INTO users (key, value) VALUES ('Language_1', 'Farsi');
INSERT INTO users (key, value) VALUES ('Language_2','English');

