CREATE TABLE IF NOT EXISTS investments(
    inv_id INTEGER,
    investor TEXT NOT NULL,
    shares INTEGER NOT NULL
    FOREIGN KEY(stock_id) REFERENCES stocks(id)
);

INSERT INTO stocks (id, symbol, sector)
SELECT id, symbol, sector FROM companies;