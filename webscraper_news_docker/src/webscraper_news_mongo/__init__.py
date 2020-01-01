from api import app
#import logging

#from config import Config, LOG_FORMAT

#logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def start_app():
    #logging.info("Starting scraper")
    app.run(
        host='0.0.0.0',
        port='5000',
        debug=False,
        use_reloader=False
    )
