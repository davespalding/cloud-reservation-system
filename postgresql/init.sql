CREATE DATABASE reserv OWNER postgres;
\c reserv;

CREATE EXTENSION IF NOT EXISTS hstore;

CREATE TABLE IF NOT EXISTS info (
    metadata HSTORE NOT NULL DEFAULT hstore(''),
    stock HSTORE NOT NULL DEFAULT hstore(''));
INSERT INTO info (metadata, stock) VALUES (
    hstore('schema_ver', '1'),
    hstore('reserved', '0'));

CREATE TABLE IF NOT EXISTS ids (
    order_id VARCHAR(12) PRIMARY KEY,
    number VARCHAR(12) NOT NULL);

CREATE INDEX numbers_idx ON ids USING HASH (number);
