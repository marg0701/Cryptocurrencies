
# ******************************************************************************
#                           Facebook Prophet                                   *
# ******************************************************************************

# ------------------------------------------------------------------------------
#                                Packages

from flask import Flask,jsonify,render_template,request,Response

# Package for managing dataframes
import pandas as pd

import datetime
import dateutil
from datetime import date, timedelta

import requests

import logging
import time
import json

import portfolio_functions

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
#-------------------------------------------------------------------------------
#                            Applying the algorithm

def portfolio():

    logging.info("Starting portfolio...")

    coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin-cash']
    #coins = ['bitcoin']

    dic = {}

    for coin in coins:
        if coin == 'bitcoin-cash':
            coin = 'bitcoin_cash'

        req = requests.get('http://sqls:5003/querydf/{}'.format(coin))
        jonson = json.loads(req.text)
        coin_info = pd.read_json(jonson["result"])

        if coin == 'bitcoin':
            coin_info["DATE_INFO"] = coin_info["DATE_INFO"].apply(lambda x: datetime.datetime.fromtimestamp(x/1e3))
            dic["Date"]=coin_info["DATE_INFO"]

        dic[coin]=coin_info["CLOSE"]

    df = pd.DataFrame.from_dict(dic)
    df=df[df['Date'] > (datetime.datetime.today() + dateutil.relativedelta.relativedelta(years=-1))]
    logging.info(df.head())
    logging.info(df.tail())
    portfolio_functions.portfolio_all(df)

time.sleep(80)
portfolio()
