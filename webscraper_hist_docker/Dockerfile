FROM python:3.7

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install BeautifulSoup4
RUN pip install apscheduler

ADD . /app
RUN python setup.py develop

EXPOSE 5000
CMD ["start-webscraper_hist"]
