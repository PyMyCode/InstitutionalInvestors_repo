# Institutional Investor Analyzer

#### Video Demo:  https://youtu.be/jSbV49E-1PM
#### Description:
A web aplication that gives an overview of the S&P500 stocks and the institutional investors invested in them.

### Overview

The web application is build on the [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework. The backend mainly uses [Python](https://www.python.org/) with a [Sqlite](https://www.sqlite.org/index.html) database. The frontend is mainly HTML and CSS under the [Bootstrap](https://getbootstrap.com/) framework.

The main Python package used to get stock market data is [yfinance](https://pypi.org/project/yfinance/). It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes.

### database.db

The database consists can be found in *static* folder and consists of 3 tables.

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

The *inst_investors* table consists of all the institutional investors invested in the s&p500 stocks. Each institutional investors has unique id and a name.

The *investments* table consists shows the investments (stock and shares) of all the institutional investors.

The sql queries used to create the database are also stored in the same folder for reference.

### app.py

This is the main file of the Flask application. 

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
Then the SQL database is connected. However, first the base directory to */static* for the sql queries.
```python
# connecting to SQL database
try:
    db = sqlite3.connect(db_path, check_same_thread=False)
    cur = db.cursor()
except Error as e:
    print(e)
```

Now the first */* route calls the *index()* function that renders the *index.html* which can be found in the */templates* folder. This is the landing pade of the user (Homepage).

```python
@app.route("/")
def index():
        
    # rendering the index template
    return render_template("index.html")
```

The first overview that the web application show is that of all the s&p500 stocks. In order to the do that, a function called *company_oveview()* is called when going to the */company_overview* route (by clicking *Companies* on the navigation bar).

