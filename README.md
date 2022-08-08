# Institutional Investor Analyzer

#### Video Demo:  https://youtu.be/jSbV49E-1PM
## Description:
A web aplication that gives an overview of the S&P500 stocks and the institutional investors invested in them.

### Overview

The web application is build on the [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework. The backend mainly uses [Python](https://www.python.org/) with a [Sqlite](https://www.sqlite.org/index.html) database. The frontend is mainly HTML and CSS under the [Bootstrap](https://getbootstrap.com/) framework.

The main Python package used to get stock market data is [yfinance](https://pypi.org/project/yfinance/). It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes.

### database.db

The database can be found in *static* folder and consists of 3 tables.

```console
$ cd /static
/static$ sqlite3 database.db
SQLite version 3.31.1
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE stocks(
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    sector TEXT
, name TEXT);
CREATE TABLE inst_investors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
    );
CREATE TABLE investments (
    inst_investors_id INTEGER,
    stocks_id INTEGER,
    shares INTEGER,
    FOREIGN KEY(inst_investors_id) REFERENCES inst_investors(id),
    FOREIGN KEY(stocks_id) REFERENCES stocks(id));
```

The *stock* table consists of all the s&p500 stocks. Each stock has been assigned an unique id along with a symbol ("like *AAPL* for Apple Inc.") that is used to get stock data via yfinance.

The *inst_investors* table consists of all the institutional investors invested in the s&p500 stocks. Each institutional investors has a unique id and a name.

The *investments* table consists shows the investments (stock and shares) of all the institutional investors.

The sql queries used to create the database are also stored in the */workfiles* folder for reference.

### app.py

This is the main file of the Flask application. A step by step explanation is given below.

First the required modules are imported
```python
from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
import os.path
import sys
from yfinance import Ticker
import pandas as pd
```
The flask application is initialized.
```python
#initilazing Flask app
app = Flask(__name__)
```
Then the SQL database is connected. However, the base directory used to execute the sql queries is changed to */static*.
```python
# connecting to SQL database
try:
    db = sqlite3.connect(db_path, check_same_thread=False)
    cur = db.cursor()
except Error as e:
    print(e)
```

Now the first */* route calls the *index()* function that renders the *index.html* which can be found in the */templates* folder. This is the landing page of the user (Homepage).

```python
@app.route("/")
def index():
        
    # rendering the index template
    return render_template("index.html")
```

The first overview that the web application shows is all the s&p500 stocks. In order to the do that, a function called *company()* is called when going to the */company* route (by clicking *Companies* on the navigation bar).

The function gets the *id, symbol, name* of all the stocks from the *stocks* table and displays on the webpage.

```python
@app.route("/companies")
def companies():

    # Getting stock list
    stocks_list = cur.execute("SELECT id, symbol, name FROM stocks ORDER BY symbol")

    # rendering the index template
    return render_template("companies.html", stocks_list = stocks_list)
```
When the user clicks any of the stocks, they are redirected to the */company_overview* route that calls *company_overview()* function. The function also gets the *stock_id* of the respective stock via the *POST* method. Using the *stock_id*, the *stock_symbol* is extracted from the database.

The stock_symbol is used to create a Ticker object that allows the user to access stock ticker data using the yfinance library.

The *.info* and *.institutional_holders* attributes if the *Ticker()* object as then used to extract market and investor information of the stock. These are then rendered to the frontend.

```python
@app.route("/company_overview", methods=["POST"])
def company_oveview():

    stock_id = request.form.get("stock_id")
    
    # getting stock details
    stock_symbol = cur.execute("SELECT symbol FROM stocks WHERE id = ?", [stock_id]).fetchone()[0]
    
    # creating the Ticker Object
    t = Ticker(stock_symbol)

    # getting stock info
    stock_info = t.info

    # converting marketcap
    stock_info["marketCap"] = stock_info["marketCap"] / (10**9)

    # converting marketcap
    stock_info["sharesOutstanding"] = stock_info["sharesOutstanding"] / (10**6)

    # getting institutional ivestors
    df = t.institutional_holders

    #converting shares to millions
    df["Shares"] = df["Shares"] / (10**6)

    # % of shares to outsanding shares
    df["Shares_percentage"] = (df["Shares"] / stock_info["sharesOutstanding"])*100

    #converting shares to millions
    df["Value"] = df["Value"] / (10**9)

    # rendering the template
    return render_template("company_overview.html", stock_info = stock_info, inv_list = df.values.tolist())
```
The second overview that the web application shows all the institutional investors invested in the s&p500 stocks. In order to the do that, a function called *investors()* is called when going to the */investors* route (by clicking *Companies* on the navigation bar).

The function gets the *id, name* of all the institutional investors from the *inst_investors* table and displays on the webpage.
```python
@app.route("/investors")
def investors():

    # Getting stock list
    investors_list = cur.execute("SELECT id, name FROM inst_investors ORDER BY name")
    
    # rendering the index template
    return render_template("investors.html", investors_list = investors_list)
```
When the user clicks on any of the institutional investors, they are redirected to the */investor_overview* route that calls *investor_overview()* function. The function also gets the *inv_id* of the respective stock via the *POST* method. Using the *inv_id*, all the investments of the investor are extracted from the *investments* table and rendered to the frontend.

```python
@app.route("/investor_overview", methods=["POST"])
def investor_overview():

    # fetching inv id
    inv_id = request.form.get("inv_id")

    investor_name = cur.execute("SELECT name FROM inst_investors WHERE id = ?", [inv_id]).fetchone()[0]

    # fetching investments from database
    investments = cur.execute("SELECT  symbol, stocks.name, shares, stocks.id FROM investments JOIN stocks ON investments.stocks_id = stocks.id WHERE inst_investors_id = ? ORDER BY stocks.name", [inv_id]).fetchall()

    # convertign shares to millions
    investments_list = []
    for investment in investments:
        investment = list(investment)
        investment[2] = investment[2] / (10**6)
        investments_list.append(investment)

    return render_template("investor_overview.html", investor_name = investor_name, investments_list = investments_list)
```