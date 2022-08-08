CREATE TABLE IF NOT EXISTS inst_investors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
    );

INSERT INTO inst_investors (name)
SELECT DISTINCT(Holder) FROM investors ORDER BY Holder;