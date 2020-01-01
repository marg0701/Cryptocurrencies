from flask import Flask, request
import requests
import pandas as pd
import sqlalchemy
from sql_historical_functions import create_table
from sqlalchemy import create_engine,types
import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
create_table()
logging.info("ha salido de create_table")

@app.route("/login", methods=['POST'])

def login():
    logging.info("Entra a validate...   ")
    logging.info("Antes de establecer comunicacion a la db...")
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    conn = engine.connect()
    conn.execute("commit")
    logging.info("Conexion establecida a la db...")

    if request.method == 'POST':
##################################################
        data_received=request.get_json()

        logging.info("Obtuvo el json del template html...")
        logging.info(data_received)

        data_to_check=list(data_received.values())[0]
        logging.info(data_to_check)

        email_to_check=data_to_check[0]
        logging.info(email_to_check)

        password_to_check=data_to_check[1]
        logging.info(password_to_check)

        logging.info("han sido separados el email y el password...")

    ##################################################
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
            logging.info("compara email y contraseña")
            
            if data["EMAIL"] ==email_to_check and data["PASSWORD"] == password_to_check:
                user_session=1

                logging.info("Resultado de session: .... ")
                logging.info(user_session)
                

                logging.info("Ha sido verificado el usuario")
            
            else:

                user_session=0
                logging.info("Resultado de session: .... ")
                logging.info("Algun dato no es valido ... ")
                logging.info(user_session)
                

        else:

            logging.info("user_session cuando no encuentra el usuario o la contraseña")
            user_session=0
            logging.info(user_session)
    
    return 'data has been registered correctly'

# ##################################################
#         #logging.info("Inicia la comparación del mail...")
#     if db_email.fetchone() is None:
#         user_status=0
#         logging.info("user_status=0")
#     else:
#         user_status=1
#         logging.info("user_status=1")
# ##################################################
#     logging.info("Inicia la comparación del usuario con contraseña...")
#     if (email_to_check == db_email and password_to_check == db_password and user_status == 1):

#         session_status=1
#         logging.info("session_status =1")
#     else:
#         session_status=0
#         logging.info("session_status=0")
# ##################################################
#     logging.info("Sale de la comparación")
#     full_info={"user_status":user_status,"session_status":session_status}
#     logging.info("regresa el resultado en un json: full_info ")

    return user_session


@app.route("/signin", methods=['POST'])
#logging.info("Inicia la ruta: signin...")

def signin():
    logging.info("inicia el signin... ")
    # engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    # conn = engine.connect()
    # logging.info("Entra a validate...   ")
    # logging.info("Antes de establecer comunicacion a la db...")
    # engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    # conn = engine.connect()
    # conn.execute("commit")
    # logging.info("Conexion establecida a la db...")

    if request.method == 'POST':
        
        data_received=request.get_json()
        logging.info("Obtiene el json")
        logging.info(data_received)
        
        logging.info("valores para insertar....")
        #data_to_insert=list(data_received.values())[0]
        logging.info(data_received)
        
        col=['NAME', 'LASTNAME','EMAIL', 'PASSWORD', 'PHONE' , 'COUNTRY']
        val =pd.DataFrame.from_dict(data_received, orient='index',columns=col)

        #values = pd.DataFrame(data_to_insert)
        logging.info("transforma el json a DataFrame")
        logging.info(val)
        
        logging.info("Comienza la conexion a la db")
        engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
        conn = engine.connect()
        conn.execute("commit")
        
        #logging.info("Conexión finalizada...")
        logging.info("la tabla contiene...")
        result=conn.execute('SELECT * from USERS').fetchall() 
        logging.info(result)

        logging.info("Inserta los datos...")
        val.to_sql('USERS',con=engine,index=False,if_exists='append')
        logging.info("datos insertados...")
        
        logging.info("la tabla ahora contiene...")
        result2=conn.execute('SELECT * from USERS').fetchall() 
        logging.info(result2)


        #values
        #conn.close()
        logging.info("cierra la conexión")

        return 'the user has been registered'