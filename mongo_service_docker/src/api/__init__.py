# from newspaper import Article ,fulltext
# import newspaper
# import pandas as pd
from pymongo import MongoClient
import json
from flask import Flask, render_template, request
import requests
import logging
from bson.json_util import dumps
from bson import json_util

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
########################################################

client = MongoClient("mongodb://db_mongo:27017/")
db = client["news"]
news = db["news"]

db.news.delete_many({})

#######################################################

@app.route("/write_news", methods=['POST'])
def write():
    if request.method == "POST":
        logging.info("Post requested")
        raw_news=request.get_json()
        #logging.info(raw_news)
        news.insert_many(raw_news)
        return 'Ok, data has been stored correctly'


#######################################################

@app.route("/read_news", methods=['GET'])
def read():
    logging.info("Get requested")
    lr=json.loads(dumps(news.find()))
    logging.info(type(lr))
    return json.dumps(lr)

