FROM python:3.7

WORKDIR /app

ADD . /app

RUN apt-get update && \
    pip install flask_mysqldb && \
    pip install sqlalchemy && \
    pip install mysqlclient && \
    pip install .

EXPOSE 5004
CMD ["start-sql_service"]
