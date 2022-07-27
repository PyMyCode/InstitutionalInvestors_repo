from flask import Flask, redirect, render_template, request
import sqlite3
from sqlite3 import Error
import os.path
import sys
from yfinance import Ticker
import pandas as pd

from numpy import identity
#import yfinance as yf

#initilazing Flask app
app = Flask(__name__)

# connecting to SQL database
# connecting to sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, r"static/database.db")

try:
    db = sqlite3.connect(db_path, check_same_thread=False)
    cur = db.cursor()
except Error as e:
    print(e)

@app.route("/")
def index():
    
    # rendering the index template
    return render_template("index.html")

@app.route("/companies")
def companies():

    # Getting stock list
    stocks_list = cur.execute("SELECT id, symbol, name FROM stocks ORDER BY symbol")
    # print(type(stocks_list.fetchall()), file=sys.stderr)

    # rendering the index template
    return render_template("companies.html", stocks_list = stocks_list)

@app.route("/company_overview", methods=["POST"])
def company_oveview():

    stock_id = request.form.get("stock_id")
    
    # getting stock details
    stock_symbol = cur.execute("SELECT symbol FROM stocks WHERE id = ?", [stock_id]).fetchone()[0]
    #stock_symbol = stock_symbol.fetchone()[0], file=sys.stderr)
    
    print(type(stock_symbol), file=sys.stderr)

    # getting stock info
    t = Ticker(stock_symbol)
    stock_info = t.info

    # converting marketcap
    stock_info["marketCap"] = stock_info["marketCap"] / (10**9)

    # getting institutional ivestors
    df = t.institutional_holders

    #converting shares to millions
    df["Shares"] = df["Shares"] / (10**6)

    #converting shares to millions
    df["Value"] = df["Value"] / (10**9)

    # rendering the template
    return render_template("company_overview.html", stock_info = stock_info, inv_list = df.values.tolist())

#@app.route('/checkouts/<transaction_id>', methods=['GET'])
#def show_checkout(transaction_id):