'''
###########################################################################################
##     Here is the service of the Webscraper Historical prices of the cryptocurrencies   ##
##     Communication with SQL DB                                                         ##
###########################################################################################
'''

# -------------------------------- Import Packages ----------------------------------------
from flask import Flask,jsonify, render_template,request,Response
import json
import logging
import webscraper_hist_functions
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# -------------------------------- Functions ---------------------------------------------

# This funtion gives you the historical information prices (without communication with SQL)
def writedf(coin):
    logging.info("Starting webscraping...")
    histdf = webscraper_hist_functions.retrieve(coin, '1-1-2017', datetime.datetime.today().strftime('%m-%d-%Y'))
    logging.info("Webscraping succesful...")
    histdf.columns = ['DATE_INFO', 'COIN', 'OPENING', 'CLOSE', 'MIN_VALUE', 'MAX_VALUE', 'VOL', 'MARKET_CAP']
    histdf["DATE_INFO"] = histdf["DATE_INFO"].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'))
    resultjson = histdf[[ 'DATE_INFO', 'CLOSE', 'OPENING', 'MAX_VALUE', 'MIN_VALUE', 'VOL']].to_dict()
    if coin == 'bitcoin-cash':
        coin = 'bitcoin_cash'
        
    logging.info("Inserting historical info to SQL DB")
    req = requests.post('http://sqls:5003/insertdf/{}'.format(coin), json = resultjson)

    logging.info("I inserted historical data of " + coin + " in sql service")
time.sleep(15)
coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin-cash']
#coins = ['bitcoin']
for coin in coins:
    logging.info("Webscraping process for " + coin)
    writedf(coin)
