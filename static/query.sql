--AEW Capital Management, LP
CREATE TABLE investments (
    inst_investors_id INTEGER,
    stocks_id INTEGER,
    shares INTEGER,
    FOREIGN KEY(inst_investors_id) REFERENCES inst_investors(id),
    FOREIGN KEY(stocks_id) REFERENCES stocks(id))