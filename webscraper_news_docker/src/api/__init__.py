from newspaper import Article ,fulltext
import newspaper
import pandas as pd
#from pymongo import MongoClient
import json
from flask import Flask, render_template, request
import time
import random
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def news_webscraper():
        #The aim of this function is to obtain today's and relevant news about cryprocurrency behavior
        #url='https://markets.businessinsider.com/cryptocurrencies'
        #url='https://www.marketwatch.com/investing/cryptocurrency'
        #url='https://www.theguardian.com/international'
        url='https://www.economist.com/'
        cnn_paper = newspaper.build(url)

        logging.info("Consulting url")

        url_list=[]

        for article in cnn_paper.articles[0:7]:
                url_list.append(article.url)

        title_list=[]
        content_list=[]

        logging.info("Preparing news...")

        for x in url_list:
                time.sleep( random.randint(0,9) )
                art=Article(x)
                art.download()
                art.parse()
                title_list.append(art.title)
                content_list.append(art.text)

        logging.info("Obtaining news")

        news_repository_pre=list(zip(url_list,title_list,content_list))
        col=['url','title','content']

        news_repository=pd.DataFrame(news_repository_pre,columns=col)[0:7]

        news_dic=news_repository.to_dict(orient='records')
        logging.info("Starting mongo database writing")
        x=requests.post('http://mongos:5000/write_news', json=news_dic)
        logging.info(x.text)

news_webscraper()
scheduler = BackgroundScheduler()
job = scheduler.add_job(news_webscraper, 'interval', minutes=10)
scheduler.start()
