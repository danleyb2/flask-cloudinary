PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DROP TABLE IF exists cars;

CREATE TABLE "images"
(
    name VARCHAR NOT NULL,
    id INTEGER PRIMARY KEY autoincrement
    
);

CREATE TABLE "settings"
(
    id INTEGER PRIMARY KEY autoincrement,
    name VARCHAR NOT NULL,
    value VARCHAR NULL
);

COMMIT;