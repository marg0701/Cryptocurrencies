from webscraper_hist import app

def webscraper_hist_app():
    app.run(
        host='0.0.0.0',
        port='5000',
        debug=False,
    )
