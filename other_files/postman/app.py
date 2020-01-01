from flask import Flask, request
app = Flask(__name__)

# Declare SQL engine
# Declare connection
# All the endpoints here are your rules to connect to the database

@app.route("/", methods=["GET"])
def home():
    print("From home")
    return "ok"


@app.route("/get_data", methods=["POST"])
def get_data():
    print("From get data")
    return "get_data"


@app.route("/give_me_coin/<name>/<lastname>", methods=["POST"])
def get_data_coin(name,lastname):
    print(name,lastname)
    return lastname


@app.route("/give_me_coin", methods=["POST"])
def get_data_coin_dates():
    init_date = request.form.get("init_date", None)
    final_date = request.form.get("final_date", None)
    coin = request.form.get("coin", None)

    # SQL commands
    # SELECT * from Table 1 where name == coin and date > init_date and date < final_date
    result = [1,2,3,4,5,6]

    return ({
        "values": result,
        "status": "OK",
        "message": "the dates you selected are {} and {}".format(init_date, final_date),
    }, 200)

# Base64 -> str binario


if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8080,
        debug=True
    )
