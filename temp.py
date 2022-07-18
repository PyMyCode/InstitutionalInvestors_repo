from gettext import install
import yfinance as yf
import pandas as pd
import sqlite3
from sqlite3 import Error
import os.path

# connecting to sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, r"static/database.db")

try:
    db = sqlite3.connect(db_path)
except Error as e:
    print(e)

# creating a cursor
cur = db.cursor()

# getting stock symbols from sql database
try:
    # 
    stock_list = cur.execute("SELECT symbol FROM stocks").fetchall()
except Error as e:
    print(e)

#creating a sql investor table
cur.execute('CREATE TABLE IF NOT EXISTS investors (Holder TEXT)')
db.commit()

count = 58
# going through each stock in s&p500 databse
for s in stock_list:

    s = s[0]

    count += 1
    print(f"{count} {s}")

    try:
        # creating the ticker object
        t = yf.Ticker(s)

        # adding just investor name and number of shares
        inst_holders_df = t.institutional_holders[["Holder"]]

        # adding to the sql table
        inst_holders_df.to_sql("investors", db, if_exists="append", index=False) 

    except Exception as e:
        print(e)
        pass

print("FERTIG!!!")