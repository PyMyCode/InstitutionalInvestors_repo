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

# getting stock symbols from SQL database
sql_str = "SELECT symbol FROM stocks LIMIT 5"
try:
    #
    stock_list = cur.execute(sql_str).fetchall()
except Error as e:
    print(e)

# going through each stock in s&p500 databse
for s in stock_list:
    
    s = s[0]

    try:
        # creating the ticker object
        t = yf.Ticker(s)
        inst_holders_df = t.institutional_holders
    except Exception as e:
        print(e)
        break
    
    # adding ticker to the dataframe
    inst_holders_df["ticker"] = s

    try:
        # concatinating df
        df = pd.concat([df, inst_holders_df], ignore_index=True )
    except:
        # creating a df
        df = inst_holders_df

df.to_excel("output_3.xlsx")
print(df)

# closing database
db.close()