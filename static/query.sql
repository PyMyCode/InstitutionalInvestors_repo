SELECT  symbol, stocks.name, shares
FROM investments
JOIN inst_investors
    ON investments.inst_investors_id = inst_investors.id
JOIN stocks
    ON investments.stocks_id = stocks.id
WHERE inst_investors_id = 46
;