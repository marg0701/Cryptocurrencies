import pandas as pd
import json
from flask import Flask, render_template, request
import logging
import requests

logging.info("Antes de la app")
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


#######################################################
@app.route("/", methods=["GET"])
def ini():
    return 'ok'


@app.route('/login')
def login():
    logging.info("Inicia el login...")
    return render_template('login_form.html')

@app.route('/signin')
def signin():
    logging.info("Inicia el signin...")
    return render_template('signin_form.html')


@app.route('/login_to_send', methods = ['POST', 'GET'])
#logging.info("Inicia validate....")
def login_to_send():
    logging.info("Inicia validate....")
    if request.method == "POST":
        result = request.form
        logging.info("request form ....")
        result_dic=result.to_dict()
        data_received={'sent':list(result.values())}
        logging.info("por enviar dic...")
        requests.post('http://sql_service:5004/login', json=data_received) 
        logging.info("publicación de json en: http://sql_service:5004/login: json_result_dic")
    return data_received

@app.route('/signin_to_send', methods = ['POST', 'GET'])

def signin_to_send():
    logging.info("signin to send....")
    
    if request.method == "POST":
        result = request.form
        logging.info("request form ....")
        result_dic=result.to_dict()
        data_received={'sent':list(result.values())}
        logging.info("por enviar dic...")
        requests.post('http://sql_service:5004/signin', json=data_received) 
        logging.info("publicación de json en: http://sql_service:5004/signin: json_result_dic")
    return data_received    




