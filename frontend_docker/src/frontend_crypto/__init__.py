from app import server

def start_app():
    server.run(
        host='0.0.0.0',
        port='5000',
        debug=True,
    )