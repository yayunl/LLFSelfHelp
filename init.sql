-- init.sql
-- Since we might run the import many times we'll drop if exists
DROP DATABASE IF EXISTS llfdb_dev;

CREATE DATABASE llfdb_dev;

-- Make sure we're using our `blog` database
\c llfdb_dev;

-- We can create our user table
/*CREATE TABLE IF NOT EXISTS user (
  id SERIAL PRIMARY KEY,
  username VARCHAR,
  email VARCHAR
);

-- We can create our post table
CREATE TABLE IF NOT EXISTS post (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES user(id),
  title VARCHAR,
  content TEXT,
  image VARCHAR,
  date DATE DEFAULT CURRENT_DATE
);*/