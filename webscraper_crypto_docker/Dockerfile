FROM python:3.7

WORKDIR /app


RUN pip search yaml
RUN pip install pyyaml
RUN pip install --upgrade pip
RUN pip install python-binance

ADD . /app
RUN python setup.py develop

EXPOSE 5000
CMD ["start-webscraper_crypto"]
