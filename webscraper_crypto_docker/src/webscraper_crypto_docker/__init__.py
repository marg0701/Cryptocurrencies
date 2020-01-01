from webscraper_crypto import app

def webscraper_crypto_app():
    app.run(
        host='0.0.0.0',
        port='5002',
        debug=False,
    )
