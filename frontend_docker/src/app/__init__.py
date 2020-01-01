from flask import Flask, jsonify, render_template, request, url_for, Response
from bson.json_util import dumps
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import json
import requests
import logging
import pandas as pd

coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin_cash']
#coins = ['bitcoin']

logging.basicConfig(level=logging.INFO)

server = Flask(__name__)

@server.route('/')
def index():
    return render_template("index.html")


@server.route('/home', methods=["GET"])
def coin_info():
    graphresultshtml = render_template("graphresults.html")
    return json.dumps({
        "html": graphresultshtml
    })

@server.route('/home/<coin>', methods=["GET"])
def coin_graph(coin):
    logging.info("Requesting real time info for " +  coin)
    req = requests.get('http://sqls:5003/queryreal/{}'.format(coin))
    logging.info(req.text)
    jonson = json.loads(req.text)
    coin_info = pd.read_json(jonson["result"])
    logging.info(coin_info)
    with open("/appdata/graph_{}.html".format(coin), "r") as f:
        text = f.read()
    value = coin_info["PRICE"][0]
    logging.info(value)
    graphresultspercoinhtml = render_template("graphresultspercoin.html", coin=coin, text=text, value=value)
    return json.dumps({
        "html": graphresultspercoinhtml
    })


@server.route('/profile', methods=["POST"])
def my_profile():
    if request.method == "POST":

        # logging.info(" //////////////////////// ")
        # user_info=request.get_json()
        # logging.info("User info ... ")
        # logging.info(user_info)
        # logging.info("///////////////// ")
        # logging.info(" ")

        logging.info("Here in profile")
        t=open('/appdata/portinfo.json','r').read()
        portfolioinfo=json.loads(t)
        logging.info(portfolioinfo)
        weights={}
        for coin in coins:
            weights[coin]=round(float(portfolioinfo['weights'][coin]),3)
        quantities=['Return','Volatility','Sharpe Ratio']
        performance={}
        for quantitie in quantities:
            performance[quantitie]=round(float(portfolioinfo['performance'][quantitie]),3)

        with open("/appdata/portgraphstatic.html", "r") as h:
            graphtext = h.read()

        profile_text = render_template(
            "profile.html", coins = coins, weights=weights,performance=performance,graph=graphtext
        )


        return json.dumps({
            "ht ml": profile_text
        })
    
    




@server.route('/warning', methods=["GET"])
def anom_warning():
    logging.info("Reading from MongoDB")
    x=requests.get('http://mongos:5000/read_news')
    logging.info("Read finished")
    msg = list(x.json())
    logging.info(type(msg))

    warning_text = render_template(
        "warning.html", news = msg
    )
    return json.dumps({
        "html": warning_text
    })


@server.route('/portfolio', methods=["GET"])
def portfolio():

    logging.info("Here in portfolio")
    t=open('/appdata/portinfo.json','r').read()
    portfolioinfo=json.loads(t)
    logging.info(portfolioinfo)
    weights={}
    for coin in coins:
        weights[coin]=round(float(portfolioinfo['weights'][coin]),3)
    quantities=['Return','Volatility','Sharpe Ratio']
    performance={}
    for quantitie in quantities:
        performance[quantitie]=round(float(portfolioinfo['performance'][quantitie]),3)

    with open("/appdata/portgraphstatic.html", "r") as h:
        graphtext = h.read()

    portfolio_text = render_template(
        "portfolio.html",coins = coins, weights=weights,performance=performance,graph=graphtext
    )
    return json.dumps({
        "html": portfolio_text
    })


@server.route('/about', methods=["POST"])
def about():
    if request.method == "POST":

        with open("/appdata/portgraphstatic.html", "r") as h:
            graphtext = h.read()

        about_text = render_template(
            "about.html",graphtext=graphtext
        )

        return json.dumps({
            "html": about_text
        })

   