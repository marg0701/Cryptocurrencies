from flask import Flask, request
import requests
import pandas as pd
import sqlalchemy
from sql_historical_functions import create_table
from sqlalchemy import create_engine,types
import datetime
import json
import logging
import yaml
import time
import base64

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

create_table()

@app.route("/querydf/<coin>", methods=['GET'])
def index(coin):
    logging.info(request.method + " requested")
    coin = str(coin)
    coin = coin.upper()
    logging.info("Query requested for " + coin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    logging.info("Query requested: select * from " + coin)
    rows = conn.execute("select * from " + coin)
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
    dic = {}
    for k in list_of_dicts[0].keys():
        dic[k] = tuple(dic[k] for dic in list_of_dicts)
    result = pd.DataFrame(dic)
    return json.dumps({
            "result":result.to_json()
        })

@app.route("/querypred/<coin>", methods=['GET'])
def prediction(coin):
    logging.info(request.method + " requested")
    coin = str(coin)
    coin = "PRED_" + coin.upper()
    logging.info("Query requested for " + coin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    rows = conn.execute("select * from " + coin + " where DATE_P = '"+ datetime.datetime.today().strftime("%Y-%m-%d"+"'"))
    conn.close()

    list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
    dic = {}
    for k in list_of_dicts[0].keys():
        dic[k] = tuple(dic[k] for dic in list_of_dicts)
    result = pd.DataFrame(dic)
    logging.info("Query result:")
    logging.info(result)
    return json.dumps({
            "result":result.to_json()
    })

@app.route("/insertdf/<coin>", methods=['POST'])
def insert(coin):
    logging.info(request.method + " requested")
    logging.info("Inserting information of " + coin + "to SQL DB")
    resultjson = request.get_json()
    values = pd.DataFrame(resultjson)
    values["DATE_INFO"] = values["DATE_INFO"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    values["CLOSE"] = values["CLOSE"].apply(lambda x: float(x.replace(',','')))
    values["OPENING"] = values["OPENING"].apply(lambda x: float(x.replace(',','')))
    values["MAX_VALUE"] = values["MAX_VALUE"].apply(lambda x: float(x.replace(',','')))
    values["MIN_VALUE"] = values["MIN_VALUE"].apply(lambda x: float(x.replace(',','')))
    coin = str(coin)
    coin = coin.upper()
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    values.to_sql(coin,con=engine,index=False,if_exists='append')
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    return "Data insertion is complete"


@app.route("/insertpred/<predcoin>", methods=['POST'])
def insertpred(predcoin):
    logging.info(request.method + " requested")
    resultjson = request.get_json()
    values = pd.DataFrame(yaml.load(json.loads(resultjson)))
    values["ds"] = values["ds"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    values["yhat"] = values["yhat"].apply(lambda x: float(x))
    values["yhat_lower"] = values["yhat_lower"].apply(lambda x: float(x))
    values["yhat_upper"] = values["yhat_upper"].apply(lambda x: float(x))
    values.columns = ['DATE_P', 'PR_VALUE', 'DOWN_VALUE', 'UP_VALUE']
    predcoin = str(predcoin)
    predcoin = predcoin.upper()
    logging.info("Insertion requested for " + predcoin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    values.to_sql(predcoin,con=engine,index=False,if_exists='append')
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    return "Data inserted succesfuly"

@app.route("/insertreal/<realcoin>", methods=['POST'])
def insertreal(realcoin):
    logging.info("I received a request " + request.method)
    logging.info("Someone is trying to write on the DB")
    resultjson = request.get_json()
    logging.info("The info to write is:")
    logging.info(resultjson)
    values = pd.DataFrame(resultjson)
    logging.info(values.head())
    logging.info("Beginning DF transformation...")
    values["time"] = values["time"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    values["price"] = values["price"].apply(lambda x: float(x))
    values.columns = ["DATE_R", "PRICE"]
    logging.info("Result after transformation...")
    logging.info(values.head())
    realcoin = str(realcoin)
    realcoin = realcoin.upper()
    logging.info("The client is trying to write on " + realcoin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    values.to_sql("REAL_" + realcoin,con=engine,index=False,if_exists='append')
    logging.info("Data inserted")
    conn.close()
    logging.info("Connection closed")
    return "Insertion succesful"


@app.route("/queryreal/<coin>", methods=['GET'])
def readreal(coin):
    logging.info(request.method + " requested")
    coin = str(coin)
    coin = "REAL_" + coin.upper()
    logging.info("Query requested for " + coin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    rows = conn.execute("select * from " + coin + " order by DATE_R limit 1")
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
    #dic = {}
    #for k in list_of_dicts[0].keys():
    #    dic[k] = tuple(dic[k] for dic in list_of_dicts)
    result = pd.DataFrame(list_of_dicts)
    logging.info("Query result:")
    logging.info(result)
    return json.dumps({
            "result":result.to_json()
    })


################################################################
################## Servicios para el log in ####################
################################################################

#######################################################

@app.route("/login", methods=['POST'])

def login():
    logging.info("Entra a validate...   ")
    logging.info("Antes de establecer comunicacion a la db...")
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    conn = engine.connect()
    conn.execute("commit")
    logging.info("Conexion establecida a la db...")

    if request.method == 'POST':

        data_received=request.get_json()

        logging.info("Obtuvo el json del template html...")
        logging.info(data_received)

        data_to_check=list(data_received.values())[0]
        logging.info(data_to_check)

        email_to_check=data_to_check[0]
        logging.info(email_to_check)

        password_to_check=data_to_check[1]
        logging.info(password_to_check)

        logging.info("comienza a encryptar el password ...")

        pre_enc=password_to_check.encode('ascii')
        encoded=base64.b64encode(pre_enc)
        password_to_check=encoded.decode('ascii')
        logging.info(password_to_check)
        logging.info("han sido separados el email y el password...")

        result=conn.execute("SELECT EMAIL, PASSWORD from USERS where EMAIL = '" + email_to_check + "'").fetchall()
        logging.info("resultado del query")
        logging.info(result)

        if len(result)>0:
            logging.info('query no vacio')
            clean_result=result[0]
            data=[]

            for usuario in clean_result.items():
                data.append(usuario)

            logging.info("sale del for con el user y password...")
            data=dict(data)
            logging.info(data)
            logging.info("compara contraseñas")
            logging.info(data["PASSWORD"])
            logging.info(password_to_check)

            if data["EMAIL"] == email_to_check and data["PASSWORD"] == password_to_check:
                user_session=1
                logging.info("Resultado de session: .... ")
                logging.info(user_session)
                logging.info("Ha sido verificado el usuario")
                
            else:
                user_session=0
                logging.info("Resultado de session: .... ")
                logging.info("A lgun dato no es valido ... ")
                logging.info(user_session)
        else:
            logging.info("user_session cuando no encuentra el usuario o la contraseña")
            user_session=0
            logging.info(user_session)


        login_final={"result":user_session}
        #requests.post('http://localhost:5001/result', json=login_final)
        logging.info("por enviar el resultado de la autenticación ...  ")

        return login_final


@app.route("/signin", methods=['POST'])

def signin():
    logging.info("inicia el signin... ")

    if request.method == 'POST':

        data_received=request.get_json()
        logging.info("Obtiene el json ... ")
        logging.info(data_received)

        logging.info("valores para insertar ... ")

        logging.info(data_received)

        col=['NAME', 'LASTNAME','EMAIL', 'PASSWORD', 'PHONE' , 'COUNTRY']
        val =pd.DataFrame.from_dict(data_received, orient='index',columns=col)

        logging.info("lambda para encriptar los passwords ... ")

        val["PASSWORD"]=val["PASSWORD"].apply(lambda x: x.encode('ascii'))
        val["PASSWORD"]=val["PASSWORD"].apply(lambda x: base64.b64encode(x))


        logging.info("transforma el json a DataFrame")
        logging.info("Encoded ... ?")
        logging.info(val)

        logging.info("Comienza la conexion a la db")
        engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
        conn = engine.connect()
        conn.execute("commit")

        logging.info("la tabla contiene...")
        result=conn.execute('SELECT * from USERS').fetchall()
        logging.info(result)

        logging.info("Inserta los datos...")
        val.to_sql('USERS',con=engine,index=False,if_exists='append')
        logging.info("datos insertados...")

        logging.info("la tabla ahora contiene...")
        result2=conn.execute('SELECT * from USERS').fetchall()
        logging.info(result2)

        logging.info("cierra la conexión")
        #return redirect("http://localhost:5001/login")
        #webbrowser.open('http://localhost:5001/login')
        result={"result":"ok"}

        return result

@app.route("/user_info", methods=['GET'])

def user_info():
        logging.info("inicia el proceso user_info ... ")
        logging.info("Antes de establecer comunicacion a la db...")
        
        engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
        conn = engine.connect()
        conn.execute("commit")
        
        logging.info("Conexion establecida a la db...")

        data_received=request.get_data()

        logging.info("Obtuvo el json del login ... (user info)")
        logging.info(data_received)


        email_to_check=data_received.decode('ascii')
        logging.info(email_to_check)


        result_user=conn.execute("SELECT * from USERS where EMAIL = '" + email_to_check + "'").fetchall()

        result_user2=result_user[0]

        data_2=[]
        for usuario in result_user2.items():
            print(usuario)
            data_2.append(usuario)
        data_2=dict(data_2)

        del data_2["PASSWORD"]


        logging.info("información excepto el password")
        logging.info(data_2)
        return data_2



