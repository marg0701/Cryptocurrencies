'''
#########################################################################################
##     In this section there are the functions to webcraping the real-time values of   ##
##     the cryptocurrencies (with Binance)                                             ##
#########################################################################################
'''

# ----------------------------- Import Packages ----------------------------------------
import pandas as pd
import math
import os.path
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
import numpy as np
import logging

# Email libraries
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO)

# -------------------------------------------------------
# Email variables

MY_ADDRESS = 'uzmar.gomez@softtek.com'
PASSWORD = 'Poirot25092015@'

user_info = "contacts.txt"
email_message = "template_email.txt"

host_address = "smtp.office365.com"
port = 587

#---------------------------------------------------------

binance_api_key = 'pAtN761JV67xkRYnF4hI8RHL0DmInhHRoV50yPpz6VijEilHQdiHL7WIa4Ho60Om'    #Enter your own API-key here
binance_api_secret = 'o3juMWdjvpOhI1jfhHKwN6uereY31BSvwsDHaWWF6ytO150Y4xV1Ig3yWCtdaWwW' #Enter your own API-secret here

binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

# ------------------------------- Functions -----------------------------------------------
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new

def get_all_binance(symbol, kline_size, save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    print('All caught up..!')
    return data_df

def return_real_value(abcoin):
    trades = binance_client.get_recent_trades(symbol=abcoin)
    df = pd.DataFrame(trades)[["time","price"]]
    #df['time'] = df['time'].apply(lambda x: pd.to_datetime(x, unit='ms'))
    return df[-1:]

def send_email(real_value, pred_table):
    logging.info("Enter the send_email function")
    names, emails = get_contacts(user_info) # read contacts
    message_template = read_template(email_message)

    if float(real_value) > float(pred_table["UP_VALUE"]):
        logging.info("There was an anomaly (the real value is bigger than the prediction)")
        anomaly = 1
        importance = ( real_value - float(pred_table["UP_VALUE"]) ) / real_value
    elif float(real_value) < float(pred_table["DOWN_VALUE"]):
        logging.info("There was an anomaly (the real value is smaller than the prediction)")
        anomaly = -1
        importance = ( float(pred_table["DOWN_VALUE"]) - real_value ) / real_value
    else:
        logging.info("There was no anomaly")
        anomaly = 0
        importance = 0

    logging.info(anomaly)
    logging.info(importance)

    if anomaly !=0:
        logging.info("Going to send email")
        # set up the SMTP server
        server = smtplib.SMTP(host=host_address, port=port)
        # Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
        server.starttls()
        # Log in on an SMTP server that requires authentication
        server.login(MY_ADDRESS, PASSWORD)
        # For each contact, send the email:
        for name, email in zip(names, emails):
            logging.info("Sending email to " + name)
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(person_name=name.title())

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=email

            if importance  >= .66:
                msg['Subject']="BET Urgent Information "
                msg['X-Priority']='1'
            elif  importance > .33 and importance < .66:
                msg['Subject']="BET Important Information"
                msg['X-Priority']='3'
            elif importance  < .33:
                msg['Subject']="BET Information"
                msg['X-Priority']='5'

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            server.send_message(msg)
            del msg

        # Terminate the SMTP session and close the connection
        server.quit()
        logging.info("Email alert sended")
    elif anomaly == 0:
        logging.info("There was no anomaly")

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
