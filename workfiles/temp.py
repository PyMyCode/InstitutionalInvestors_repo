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
    stock_list = cur.execute("SELECT * FROM stocks").fetchall()
except Error as e:
    print(e)

count = 0

for s in stock_list:

    #stopper
    count += 1
    if count % 10 == 0:
        print("check!!!")


    # tracker
    print(f"{s[0]} {s[1]}")
    
    try:
        # creating the ticker object
        t = yf.Ticker(s[1])

        #-----------ADDING NAME TO stocks
        #check if already exists
        test = cur.execute('SELECT name FROM stocks WHERE id = ?', [str(s[0])])
        # if no then adding name to database
        if test.fetchall()[0][0] == None:
            # getting stock name from yfinance
            info = t.info
            name = info["longName"]
            # adding to database
            cur.execute('UPDATE stocks SET name = ? WHERE id = ?', (name, str(s[0])))
            db.commit()
        
        #-----------ADDING data TO investment table 
        #get investor data for the stock
        df = t.institutional_holders[["Holder", "Shares"]]

        #iterating through the df
        for index, row in df.iterrows():

            try:
                # getting investor id
                inst_investors_id = cur.execute("SELECT id FROM inst_investors WHERE name LIKE ?", [row["Holder"]]).fetchall()[0][0]
                print(inst_investors_id)
            except:
                # adding investor if does not exists
                cur.execute("INSERT INTO inst_investors (name) VALUES (?)", [row["Holder"]])
                db.commit()
                print("new investor added")

            # adding to the investors
            cur.execute("INSERT INTO investments (inst_investors_id, stocks_id, shares) VALUES (?, ?, ?)", (str(inst_investors_id), str(s[0]), str(row["Shares"])))
            db.commit()

    except Exception as e:
        print(e)
        break
        #db.close()
        
    #if all went well
    print("successful")

db.close()

print("FERTIG!!!")