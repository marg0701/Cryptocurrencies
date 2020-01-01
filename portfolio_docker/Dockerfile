FROM python:3.7

WORKDIR /app

ADD . /app
RUN pip install python-dateutil
RUN pip install -U scikit-learn
RUN pip install PyPortfolioOpt
RUN pip install plotly
RUN python setup.py develop

EXPOSE 5000
CMD ["start-portfolio"]
