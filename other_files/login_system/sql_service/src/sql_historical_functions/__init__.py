import csv
import pandas as pd
import logging
import sqlalchemy
from sqlalchemy import create_engine,types
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def create_table():
    logging.info("Inicia la conexion en create table...")
    #create an engine as usual with a user that has the permissions to create a database:
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306')
    logging.info("ya ha creado la conexion...")
    #You cannot use engine.execute() however, because postgres does not allow you to create
    #databases inside transactions, and sqlalchemy always tries to run queries in a transaction.
    #To get around this, get the underlying connection from the engine:
    conn = engine.connect()
    #But the connection will still be inside a transaction, so you have to end the open transaction with a commit:
    conn.execute("commit")
    #And you can then proceed to create the database using the proper SQL command for it.
    conn.execute("create database if not exists crypto")
    logging.info("ha creado la base de datos...")
    conn.execute("use crypto")
    # conn.execute("create table if not exists BITCOIN (DATE_INFO DATE, CLOSE DECIMAL(15,2), OPENING DECIMAL(15,2), MAX_VALUE DECIMAL(15,2), MIN_VALUE DECIMAL(15,2), VOL VARCHAR(20), VAR DECIMAL(6,5))")
    # conn.execute("create table if not exists ETHEREUM (DATE_INFO DATE, CLOSE DECIMAL(15,2), OPENING DECIMAL(15,2), MAX_VALUE DECIMAL(15,2), MIN_VALUE DECIMAL(15,2), VOL VARCHAR(20), VAR DECIMAL(6,5))")
    # conn.execute("create table if not exists IOTA (DATE_INFO DATE, CLOSE DECIMAL(15,2), OPENING DECIMAL(15,2), MAX_VALUE DECIMAL(15,2), MIN_VALUE DECIMAL(15,2), VOL VARCHAR(20), VAR DECIMAL(6,5))")
    # conn.execute("create table if not exists BITCOIN-CASH (DATE_INFO DATE, CLOSE DECIMAL(15,2), OPENING DECIMAL(15,2), MAX_VALUE DECIMAL(15,2), MIN_VALUE DECIMAL(15,2), VOL VARCHAR(20), VAR DECIMAL(6,5))")
    # conn.execute("create table if not exists RIPPLE (DATE_INFO DATE, CLOSE DECIMAL(15,2), OPENING DECIMAL(15,2), MAX_VALUE DECIMAL(15,2), MIN_VALUE DECIMAL(15,2), VOL VARCHAR(20), VAR DECIMAL(6,5))")
    # conn.execute("create table if not exists LITECOIN (DATE_INFO DATE, CLOSE DECIMAL(15,2), OPENING DECIMAL(15,2), MAX_VALUE DECIMAL(15,2), MIN_VALUE DECIMAL(15,2), VOL VARCHAR(20), VAR DECIMAL(6,5))")
    #conn.execute("create table if not exists USERS (USERID int NOT NULL AUTO_INCREMENT , NAME VARCHAR(20) NOT NULL, EMAIL VARCHAR(20) NOT NULL, PASSWORD VARCHAR(20) NOT NULL, PHONE VARCHAR(20) NOT NULL, COUNTRY VARCHAR(20) NOT NULL, PRIMARY KEY (USERID))")
    conn.execute("create table if not exists USERS (NAME VARCHAR(20) NOT NULL, LASTNAME VARCHAR(20) NOT NULL,EMAIL VARCHAR(20) NOT NULL, PASSWORD VARCHAR(20) NOT NULL, PHONE VARCHAR(20) NOT NULL, COUNTRY VARCHAR(20) NOT NULL, PRIMARY KEY (EMAIL))")
    logging.info("ha creado la tabla USERS...")
    conn.close()
    #engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')


