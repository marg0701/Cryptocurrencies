FROM python:3.7

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

RUN python setup.py develop

EXPOSE 5000

CMD ["start-service"]
