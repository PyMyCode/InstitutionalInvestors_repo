CREATE TABLE IF NOT EXISTS stocks(
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    sector TEXT
);

INSERT INTO stocks (id, symbol, sector)
SELECT id, symbol, sector FROM companies;