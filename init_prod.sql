-- init_prod.sql
-- Since we might run the import many times we'll drop if exists
DROP DATABASE IF EXISTS llfdb_prod;

CREATE DATABASE llfdb_prod;

\c llfdb_prod;