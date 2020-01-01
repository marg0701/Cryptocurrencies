# ******************************************************************************
#

from flask import Flask,jsonify, render_template,request,Response
import json
import logging
import timeseries_functions
import requests
import pandas as pd
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def timeseriesmodel():
    resultjson={}
    coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin-cash']
    #coins = ['bitcoin']
    for coin in coins:
        if coin == 'bitcoin':
            growth = 'linear'
            seasonality_mode= 'multiplicative'
            seasonality_prior_scale = 15.0
            holidays_prior_scale = 0.02
            changepoint_prior_scale = 0.1
            interval_width = 0.90

        elif coin == 'ethereum':
            growth = 'linear'
            seasonality_mode= 'additive'
            seasonality_prior_scale = 10.0
            holidays_prior_scale = 0.02
            changepoint_prior_scale = 0.1
            interval_width = 0.90

        elif coin == 'ripple':
            growth = 'logistic'
            seasonality_mode= 'additive'
            seasonality_prior_scale = 10.0
            holidays_prior_scale = 0.02
            changepoint_prior_scale = 0.8
            interval_width = 0.85

        elif coin == 'litecoin':
            growth = 'logistic'
            seasonality_mode= 'additive'
            seasonality_prior_scale = 10.0
            holidays_prior_scale = 0.02
            changepoint_prior_scale = 0.3
            interval_width = 0.90

        elif coin == 'iota':
            growth = 'linear'
            seasonality_mode= 'additive'
            seasonality_prior_scale = 10.0
            holidays_prior_scale = 0.02
            changepoint_prior_scale = 0.1
            interval_width = 0.90

        elif coin == 'bitcoin-cash':
            growth = 'linear'
            seasonality_mode= 'additive'
            seasonality_prior_scale = 10.0
            holidays_prior_scale = 0.02
            changepoint_prior_scale = 0.1
            interval_width = 0.90

        logging.info("Going to get info for " + coin)

        if coin == 'bitcoin-cash':
            coin = 'bitcoin_cash'

        req = requests.get('http://sqls:5003/querydf/{}'.format(coin))

        jonson = json.loads(req.text)

        coin_info = pd.read_json(jonson["result"])
        coin_info["DATE_INFO"] = coin_info["DATE_INFO"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1e3))

        logging.info("Accessed the historical data of " + coin)

        coin_df = timeseries_functions.model_from_coin(coin,coin_info,
                    growth,None,0.8,seasonality_mode,seasonality_prior_scale,holidays_prior_scale,
                    changepoint_prior_scale,interval_width)

        resultjson = coin_df.to_json()

        coin = 'pred_' + coin

        if coin == 'bitcoin-cash':
            coin = 'pred_bitcoin_cash'

        logging.info("Going to insert data from " + coin + " timeseries to SQL DB")
        requests.post('http://sqls:5003/insertpred/{}'.format(coin), json = json.dumps(resultjson))
        logging.info("Finish inserting data from prediction")


time.sleep(30)
# while True:
#     try:
#         timeseriesmodel()
#         scheduler = BackgroundScheduler()
#         job = scheduler.add_job(timeseriesmodel, 'interval', days=1)
#         scheduler.start()
#         break
#     except:
#         logging.info("Ya intente el time_series")
#         time.sleep(10)
timeseriesmodel()
