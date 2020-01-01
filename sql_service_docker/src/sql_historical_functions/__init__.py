import csv
import pandas as pd
import logging
import sqlalchemy
from sqlalchemy import create_engine,types
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def create_table():
    #create an engine as usual with a user that has the permissions to create a database:
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306')
    #You cannot use engine.execute() however, because postgres does not allow you to create
    #databases inside transactions, and sqlalchemy always tries to run queries in a transaction.
    #To get around this, get the underlying connection from the engine:
    conn = engine.connect()
    #But the connection will still be inside a transaction, so you have to end the open transaction with a commit:
    conn.execute("commit")
    #And you can then proceed to create the database using the proper SQL command for it.
    conn.execute("drop database if exists crypto")
    conn.execute("create database if not exists crypto")
    conn.execute("use crypto")

    conn.execute("create table if not exists BITCOIN (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20))")
    conn.execute("create table if not exists ETHEREUM (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20))")
    conn.execute("create table if not exists IOTA (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20))")
    conn.execute("create table if not exists BITCOIN_CASH (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20))")
    conn.execute("create table if not exists RIPPLE (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20))")
    conn.execute("create table if not exists LITECOIN (DATE_INFO DATE, CLOSE DECIMAL(15,6), OPENING DECIMAL(15,6), MAX_VALUE DECIMAL(15,6), MIN_VALUE DECIMAL(15,6), VOL VARCHAR(20))")

    conn.execute("create table if not exists PRED_BITCOIN (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    conn.execute("create table if not exists PRED_ETHEREUM (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    conn.execute("create table if not exists PRED_IOTA (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    conn.execute("create table if not exists PRED_BITCOIN_CASH (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    conn.execute("create table if not exists PRED_RIPPLE (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")
    conn.execute("create table if not exists PRED_LITECOIN (DATE_P DATE, PR_VALUE DECIMAL(15,6), UP_VALUE DECIMAL(15,6), DOWN_VALUE DECIMAL(15,6))")

    conn.execute("create table if not exists REAL_BITCOIN (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    conn.execute("create table if not exists REAL_ETHEREUM (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    conn.execute("create table if not exists REAL_IOTA (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    conn.execute("create table if not exists REAL_BITCOIN_CASH (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    conn.execute("create table if not exists REAL_RIPPLE (DATE_R DATETIME, PRICE DECIMAL(15,6))")
    conn.execute("create table if not exists REAL_LITECOIN (DATE_R DATETIME, PRICE DECIMAL(15,6))")

    conn.execute("create table if not exists USERS (NAME VARCHAR(20) NOT NULL, LASTNAME VARCHAR(20) NOT NULL,EMAIL VARCHAR(200) NOT NULL, PASSWORD VARCHAR(20) NOT NULL, PHONE VARCHAR(20) NOT NULL, COUNTRY VARCHAR(20) NOT NULL, PRIMARY KEY (EMAIL))")
    #conn.execute("create table if not exists USERS (INDEX INT, NAME VARCHAR(40), E_MAIL VARCHAR(40), PASSWORD VARCHAR(40), PHONE VARCHAR(15), COUNTRY VARCHAR(40))")

    conn.close()
    logging.info("All SQL tables created")
    #engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')

# # BITCOIN
# def bitcoin ():
#     df = pd.read_excel("bases cryptocurrencies/Bitcoin.xlsx")


#     df['DATE_INFO'] = df['DATE_INFO'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#     # Converting CLOSE, OPENING, MAX_VALUE, MIN_VALUE, VAR
#     df['CLOSE'] = df['CLOSE'].apply(lambda x: float(x))
#     df['OPENING'] = pd.to_numeric(df['OPENING'], errors='coerce')
#     df['MAX_VALUE'] = pd.to_numeric(df['MAX_VALUE'], errors='coerce')
#     df['MIN_VALUE'] = pd.to_numeric(df['MIN_VALUE'], errors='coerce')
#     df['VAR'] = pd.to_numeric(df['VAR'], errors='coerce')


#     return df.to_sql('BITCOIN',con=engine,index=False,if_exists='append')
#     logging.info("DONE")

# #ETHERUM
# def etherum ():
#     df = pd.read_excel("bases cryptocurrencies/Etherum.xlsx")

#     df['DATE_INFO'] = df['DATE_INFO'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#     # Converting CLOSE, OPENING, MAX_VALUE, MIN_VALUE, VAR
#     df['CLOSE'] = df['CLOSE'].apply(lambda x: float(x))
#     df['OPENING'] = pd.to_numeric(df['OPENING'], errors='coerce')
#     df['MAX_VALUE'] = pd.to_numeric(df['MAX_VALUE'], errors='coerce')
#     df['MIN_VALUE'] = pd.to_numeric(df['MIN_VALUE'], errors='coerce')
#     df['VAR'] = pd.to_numeric(df['VAR'], errors='coerce')

#     return df.to_sql('ETHERUM',con=engine,index=False,if_exists='append')
#     logging.info("DONE")

# #RIPPLE
# def ripple ():
#     df = pd.read_excel("bases cryptocurrencies/Ripple.xlsx")

#     df['DATE_INFO'] = df['DATE_INFO'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#     # Converting CLOSE, OPENING, MAX_VALUE, MIN_VALUE, VAR
#     df['CLOSE'] = df['CLOSE'].apply(lambda x: float(x))
#     df['OPENING'] = pd.to_numeric(df['OPENING'], errors='coerce')
#     df['MAX_VALUE'] = pd.to_numeric(df['MAX_VALUE'], errors='coerce')
#     df['MIN_VALUE'] = pd.to_numeric(df['MIN_VALUE'], errors='coerce')
#     df['VAR'] = pd.to_numeric(df['VAR'], errors='coerce')

#     return df.to_sql('RIPPLE',con=engine,index=False,if_exists='append')
#     logging.info("DONE")

# #LITECOIN
# def litecoin():
#     df = pd.read_excel("bases cryptocurrencies/Litecoin.xlsx")

#     df['DATE_INFO'] = df['DATE_INFO'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#     # Converting CLOSE, OPENING, MAX_VALUE, MIN_VALUE, VAR
#     df['CLOSE'] = df['CLOSE'].apply(lambda x: float(x))
#     df['OPENING'] = pd.to_numeric(df['OPENING'], errors='coerce')
#     df['MAX_VALUE'] = pd.to_numeric(df['MAX_VALUE'], errors='coerce')
#     df['MIN_VALUE'] = pd.to_numeric(df['MIN_VALUE'], errors='coerce')
#     df['VAR'] = pd.to_numeric(df['VAR'], errors='coerce')

#     return df.to_sql('LITECOIN',con=engine,index=False,if_exists='append')
#     logging.info("DONE")

# #IOTA
# def iota():
#     df = pd.read_excel("bases cryptocurrencies/IOTA.xlsx")

#     df['DATE_INFO'] = df['DATE_INFO'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#     # Converting CLOSE, OPENING, MAX_VALUE, MIN_VALUE, VAR
#     df['CLOSE'] = df['CLOSE'].apply(lambda x: float(x))
#     df['OPENING'] = pd.to_numeric(df['OPENING'], errors='coerce')
#     df['MAX_VALUE'] = pd.to_numeric(df['MAX_VALUE'], errors='coerce')
#     df['MIN_VALUE'] = pd.to_numeric(df['MIN_VALUE'], errors='coerce')
#     df['VAR'] = pd.to_numeric(df['VAR'], errors='coerce')

#     return df.to_sql('IOTA',con=engine ,index=False,if_exists='append')
#     logging.info("DONE")

# #BITCOIN_CASH
# def bitcoin_cash():
#     df = pd.read_excel("bases cryptocurrencies/Bitcoin cash.xlsx")

#     df['DATE_INFO'] = df['DATE_INFO'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

#     # Converting CLOSE, OPENING, MAX_VALUE, MIN_VALUE, VAR
#     df['CLOSE'] = df['CLOSE'].apply(lambda x: float(x))
#     df['OPENING'] = pd.to_numeric(df['OPENING'], errors='coerce')
#     df['MAX_VALUE'] = pd.to_numeric(df['MAX_VALUE'], errors='coerce')
#     df['MIN_VALUE'] = pd.to_numeric(df['MIN_VALUE'], errors='coerce')
#     df['VAR'] = pd.to_numeric(df['VAR'], errors='coerce')

#     return df.to_sql('BITCOIN_CASH',con=engine ,index=False,if_exists='append')
#     logging.info("DONE")


# def all_tables():
#     bitcoin()
#     etherum()
#     ripple()
#     litecoin()
#     iota()
#     bitcoin_cash()
