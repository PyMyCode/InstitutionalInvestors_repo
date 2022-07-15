from flask import Flask, redirect, render_template, request
import sqlite3
from sqlite3 import Error

#initilazing Flask app
app = Flask(__name__)
