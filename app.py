from flask import Flask, redirect, render_template, request
import sqlite3
from sqlite3 import Error
import os.path
import sys
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
    #print(type(stocks_list.fetchall()), file=sys.stderr)

    # rendering the index template
    return render_template("companies.html", stocks_list = stocks_list)

@app.route("/company_overview")
def company_oveview():

    # rendering the index template
    return render_template("company_overview.html")

#@app.route('/checkouts/<transaction_id>', methods=['GET'])
#def show_checkout(transaction_id):