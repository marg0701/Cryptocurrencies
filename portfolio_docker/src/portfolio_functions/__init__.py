import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

import plotly.graph_objects as go
import numpy as np
import plotly
import plotly.io as plio
import json

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

logging.basicConfig(level=logging.INFO)


def portfolio_all(df):

    coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin_cash']
    #coins = ['bitcoin']

    stocks = df.dropna()[coins]

    log_ret = np.log(stocks/stocks.shift(1))

    np.random.seed(42)
    num_ports = 6000
    all_weights = np.zeros((num_ports, len(stocks.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for x in range(num_ports):
        # Weights
        weights = np.array(np.random.random(len(stocks.columns)))
        weights = weights/np.sum(weights)

        # Save weights
        all_weights[x,:] = weights

        # Expected return
        ret_arr[x] = np.sum( (log_ret.mean() * weights * int(252)))

        # Expected volatility
        vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*int(252), weights)))

        # Sharpe Ratio
        sharpe_arr[x] = ret_arr[x]/vol_arr[x]

    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]
    logging.info(vol_arr)
    logging.info(ret_arr)

    fig = go.Figure(data=go.Scatter(x=vol_arr, y=ret_arr,
        mode='markers',
        marker=dict(
            size=8,
            color=sharpe_arr, #set color equal to a variable
            colorscale='Viridis', # one of plotly colorscales
            showscale=True
        )
    ))

    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[max_sr_vol],
            y=[max_sr_ret],
            marker=dict(
                color='Red',
                size=10
            ),
            showlegend=False
        )
    )

    logging.info("Saving portfolio graph...")
    plio.write_html(fig,'/appdata/portgraphstatic.html', include_plotlyjs=True)

    logging.info("Getting portfolio info")
    mu = mean_historical_return(stocks,frequency=int(252))
    S = CovarianceShrinkage(stocks).ledoit_wolf()

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    logging.info(weights)
    perf = ef.portfolio_performance(verbose=True)
    portinfo={'weights':weights, 'performance':{'Return':perf[0],'Volatility':perf[1],'Sharpe Ratio':perf[2]}}
    logging.info(type(portinfo))
    with open('/appdata/portinfo.json', 'w') as f:
        json.dump(portinfo, f)
