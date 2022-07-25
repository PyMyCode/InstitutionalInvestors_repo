SELECT   COUNT(*), inst_investors.name, inst_investors_id
FROM investments
JOIN inst_investors
    ON investments.inst_investors_id = inst_investors.id
JOIN stocks
    ON investments.stocks_id = stocks.id
GROUP BY inst_investors_id
ORDER BY COUNT(*) DESC