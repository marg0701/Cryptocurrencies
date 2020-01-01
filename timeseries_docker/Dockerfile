FROM continuumio/miniconda3

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install BeautifulSoup4
RUN pip install apscheduler
RUN conda install -c conda-forge cxx-compiler
RUN conda install -c anaconda ephem
RUN conda install -c conda-forge pystan
RUN conda install -c conda-forge fbprophet
RUN conda install -c conda-forge altair vega_datasets notebook vega
RUN conda install altair
RUN conda install vega

ADD . /app
RUN python setup.py develop

EXPOSE 5000
CMD ["start-timeseries"]
