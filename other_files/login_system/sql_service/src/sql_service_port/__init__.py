from sql_service import app

def sql_service_app():
    app.run(
        host='0.0.0.0',
        port='5004',
        debug=True,
        use_reloader=False
    )
