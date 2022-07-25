from flask import Flask, redirect, render_template, request
import sqlite3
from sqlite3 import Error

#initilazing Flask app
app = Flask(__name__)

@app.route("/")
def index():
    
    # rendering the index template
    return render_template("index.html")

@app.route("/companies")
def companies():
    
    # rendering the index template
    return render_template("companies.html")

@app.route("/company_overview")
def company_oveview():
    
    # rendering the index template
    return render_template("company_overview.html")