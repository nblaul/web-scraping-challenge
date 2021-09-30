from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

from flask import Flask
from flask import json
from flask.json import jsonify

app = Flask(__name__)

@app.route('/')

