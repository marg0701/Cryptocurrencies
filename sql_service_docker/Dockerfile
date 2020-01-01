FROM python:3.7

WORKDIR /app

ADD . /app

RUN pip search yaml
RUN pip install pyyaml
RUN pip install --upgrade pip
RUN apt-get update && \
    pip install flask_mysqldb && \
    pip install sqlalchemy && \
    pip install mysqlclient && \
    pip install .

EXPOSE 5003
CMD ["start-sql_service"]
