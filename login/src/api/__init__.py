import pandas as pd
import json
from flask import Flask, render_template, request,redirect
import logging
import requests
import webbrowser

logging.info("Antes de la app")
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


#######################################################
@app.route("/", methods=["GET"])
def ini():
    return redirect("http://localhost:5001/login", code=302)


@app.route('/login')
def login():
    logging.info("Inicia el login...")
    return render_template('login_form.html')

@app.route('/signin')
def signin():
    logging.info("Inicia el signin...")
    return render_template('signin_form.html')


@app.route('/login_to_send', methods = ['POST', 'GET'])

def login_to_send():
    logging.info("Inicia validate....")

    if request.method == "POST":
        result = request.form
        logging.info("request form ....")
        result_dic=result.to_dict()
        logging.info("result_to_dict ...")
        logging.info(result_dic)
        data_received={'sent':list(result.values())}
        user=result_dic["email"]
        logging.info("por enviar dic...")
        r=requests.post('http://sqls:5003/login', json=data_received)
        dic=r.json()
        logging.info("r=request")
        logging.info(r.text)
        logging.info("publicación de json en: http://sqls:5004/login: json_result_dic")

        if dic["result"] ==1:
            user_info=requests.post('http://sqls:5003/user_info', data=user)
            logging.info(user_info)
            a=user_info.json()
            logging.info(a)
            requests.post('http://localhost:5000/profile',json=a)
            return redirect("http://localhost:5000/", code=302)
        else:
            return redirect("http://localhost:5001/login", code=302)

@app.route('/signin_to_send', methods = ['POST'])

def signin_to_send():

    logging.info("signin to send....")

    if request.method == "POST":
        result = request.form
        logging.info("request form ....")
        result_dic=result.to_dict()
        data_received={'sent':list(result.values())}
        logging.info("por enviar dic...")
        r=requests.post('http://sqls:5003/signin', json=data_received)
        logging.info(r)
        logging.info("publicación de json en: http://sql_service_docker:5003/signin json_result_dic")
        return redirect("http://localhost:5001/login", code=302)
    