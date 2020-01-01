# ******************************************************************************
#                           Facebook Prophet                                   *
# ******************************************************************************

# ------------------------------------------------------------------------------
#                                Packages

import numpy as np

# Package for managing dataframes
import pandas as pd

# Change strings to time format
import datetime

# Facebook prophet packages (model and graphs)
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

# Plotly for graphs
import plotly
import plotly.io as plio

import bs4 as bs
import urllib.request
import pandas as pd

import plotly.offline as py
import logging

import altair as alt
from vega_datasets import data
# alt.renderers.enable('notebook')

logging.basicConfig(level=logging.INFO)


#-------------------------------------------------------------------------------
#              Applying the model to the dataframe

def model_from_coin(coin,base,growth,changepoints,changepoint_range,seasonality_mode,
                    seasonality_prior_scale,holidays_prior_scale,
                    changepoint_prior_scale,interval_width):

    df = pd.DataFrame()
    df["ds"]=base["DATE_INFO"]
    df["y"]=base["CLOSE"]

    if growth == 'logistic':
        df["cap"] = float(max(base["CLOSE"]))

    m = Prophet(growth=growth,
                changepoints=changepoints,
                changepoint_range=changepoint_range,
                yearly_seasonality=False,
                weekly_seasonality=False,
                daily_seasonality=False,
                seasonality_mode=seasonality_mode,
                seasonality_prior_scale=seasonality_prior_scale,
                holidays_prior_scale=holidays_prior_scale,
                changepoint_prior_scale=changepoint_prior_scale,
                interval_width=interval_width
                ).add_country_holidays(country_name='US'
                ).add_seasonality(name='bimonthly',period=365.25/6,fourier_order=5
                ).add_seasonality(name='yearly',period=365.25,fourier_order=3
                )

    m.fit(df)

    future = m.make_future_dataframe(periods=int(365/2))

    if growth == 'logistic':
        future["cap"] = float(max(base["CLOSE"]))

    forecast = m.predict(future)
    logging.info("Going to detect_anomalies")
    forecasted = detect_anomalies(forecast,df)
    logging.info("Saving graph for {}".format(coin))
    fig = plot_plotly(m, forecast)  # This returns a plotly Figure
    #plio.write_html(fig, '/appdata/graph_{}.html'.format(coin), include_plotlyjs=True)
    plot_anomalies(forecasted).save('/appdata/graph_{}.html'.format(coin))
    logging.info("Graph for {} saved".format(coin))
    now=datetime.datetime.now()

    resultdf=forecast[forecast['ds']==pd.Timestamp(now.year, now.month, now.day)][['ds','yhat','yhat_lower','yhat_upper']]
    return resultdf


#-------------------------------------- Anomaly detection ---------------------------------------

def detect_anomalies(forecast,base_final):
    complete = pd.merge(forecast, base_final, on='ds', how='left')
    forecasted = complete[['ds','trend', 'yhat', 'yhat_lower', 'yhat_upper', 'y']].copy()

    forecasted['anomaly'] = 0
    forecasted.loc[forecasted['y'] > forecasted['yhat_upper'], 'anomaly'] = 1
    forecasted.loc[forecasted['y'] < forecasted['yhat_lower'], 'anomaly'] = -1

    #anomaly importances
    forecasted['importance'] = 0
    forecasted.loc[forecasted['anomaly'] ==1, 'importance'] = \
        (forecasted['y'] - forecasted['yhat_upper'])/complete['y']
    forecasted.loc[forecasted['anomaly'] ==-1, 'importance'] = \
        (forecasted['yhat_lower'] - forecasted['y'])/complete['y']
    return forecasted



def plot_anomalies(forecasted):
    interval = alt.Chart(forecasted).mark_area(interpolate="basis", color = '#6C70FF').encode(
    x=alt.X('ds:T',  title ='date'),
    y='yhat_upper',
    y2='yhat_lower',
    tooltip=['ds', 'y', 'yhat_lower', 'yhat_upper']
    ).interactive().properties(
        title='Anomaly Detection'
    )

    fact = alt.Chart(forecasted[forecasted.anomaly==0]).mark_circle(size=15, opacity=0.7, color = 'Black').encode(
        x='ds:T',
        y=alt.Y('y', title='Cryptocurrency value'),
        tooltip=['ds', 'y', 'yhat_lower', 'yhat_upper']
    ).interactive()

    anomalies = alt.Chart(forecasted[forecasted.anomaly!=0]).mark_circle(size=30, color = 'Red').encode(
        x='ds:T',
        y=alt.Y('y', title='Cryptocurrency value'),
        tooltip=['ds', 'y', 'yhat_lower', 'yhat_upper'],
        size = alt.Size( 'importance', legend=None)
    ).interactive()

    return alt.layer(interval, fact, anomalies)\
              .properties(width=870, height=450)\
              .configure_title(fontSize=20)
