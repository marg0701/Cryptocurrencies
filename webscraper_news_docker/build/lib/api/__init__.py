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


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
########################################################


#######################################################

@app.route("/", methods=["GET"])
def news_webscraper():
        if request.method == "GET":
        #The aim of this function is to obtain today's and relevant news about cryprocurrency behavior
                #url='https://markets.businessinsider.com/cryptocurrencies'
                url='https://www.marketwatch.com/investing/cryptocurrency'
                #url='https://www.theguardian.com/international'
                #url='https://www.economist.com/'
                cnn_paper = newspaper.build(url)

                logging.info("Consulta url...")

                url_list=[]

                for article in cnn_paper.articles[0:7]:
                        url_list.append(article.url)

                title_list=[]
                content_list=[]

                logging.info("Preparando noticias...")

                for x in url_list:
                        logging.info("Waiting...")
                        time.sleep( random.randint(0,9) )
                        art=Article(x)
                        art.download()
                        art.parse()
                        title_list.append(art.title)
                        content_list.append(art.text)

                logging.info("Obtiene noticias")

                news_repository_pre=list(zip(url_list,title_list,content_list))
                col=['url','title','content']

                news_repository=pd.DataFrame(news_repository_pre,columns=col)[0:7]

                news_dic=news_repository.to_dic(orient='records')
                # news.insert_many(news_dic)
                logging.info("noticias a JS")
                # lr=news.find()
                x=requests.post('http://scraper:5001/', json=news_dic)
                logging.info(x.text)
                logging.info("Post...")
                return render_template('index.html')
                # if __name__=='__main__':
                #     while True:
                #         news_webscraper()
                #         time.sleep(5*60)
