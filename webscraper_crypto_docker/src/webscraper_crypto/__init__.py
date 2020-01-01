'''
###########################################################################################
##        Here is the service of the Webscraper Real-Time price of the cryptocurrencies  ##
##        Communication with SQL DB                                                      ##
###########################################################################################
'''

# --------------------------------Import Packages-------------------------------------------
from flask import Flask,jsonify, render_template,request,Response
import json
import logging
import webscraper_crypto_functions
import requests
import time
import yaml
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin_cash']

# ----------------------------------- Functions --------------------------------------------

# This function gives you the real time value of a cryptocurrency (without communication with SQL)
def get_result_from_model():
    coindict = {'bitcoin': 'BTCUSDT', 'ethereum': 'ETHUSDT', 'ripple': 'XRPUSDT', 'litecoin': 'LTCUSDT',
                'iota': 'IOTABTC', 'bitcoin_cash': 'BCHABCBTC'}
    while True:
        try:
            for coin in coins:
                logging.info("Obtaining real value for " + coin)
                df_instant_value = webscraper_crypto_functions.return_real_value(coindict[coin])
                logging.info("Values obtained:")
                logging.info(df_instant_value.head())
                logging.info(df_instant_value.columns)
                resultjson = df_instant_value.to_dict()
                logging.info("Message to be sent...")
                logging.info(resultjson)
                logging.info(type(resultjson))
                logging.info("Requesting POST...")
                x = requests.post('http://sqls:5003/insertreal/{}'.format(coin), json = resultjson)
                logging.info("POST requested...")
                logging.info("Response:")
                logging.info(x.text)
                #prediction = requests.get('http://sqls:5003/querypred/{}'.format(coin))
                #predictiondf = pd.DataFrame(yaml.load(yaml.load(prediction.text)['result']))
            break
        except:
            logging.info("I have tried the webscraper_crypto")
            time.sleep(30)
            raise    
    # webscraper_crypto_functions.send_email(float(df_instant_value['price']), predictiondf)
    # webscraper_crypto_functions.send_email(float(50000), predictiondf)
    return "OK"

#coins=['bitcoin']

time.sleep(120)
get_result_from_model()
scheduler = BackgroundScheduler()
job = scheduler.add_job(get_result_from_model, 'interval', minutes=5)
scheduler.start()

