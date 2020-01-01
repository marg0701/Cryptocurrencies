from flask import Flask, jsonify, render_template, request, url_for, Response
from bson.json_util import dumps
import dash
import dash_html_components as html
import json

server = Flask(__name__)

@server.route('/')
def index():
    if request.method == "GET":
        return render_template("index.html")

@server.route('/home', methods=["POST"])
def coin_info():
    if request.method == "POST":
        return json.dumps({
            "html": ""
        }) 

@server.route('/profile', methods=["POST"])
def my_profile():
    if request.method == "POST":
        profile_text = render_template(
            "profile.html",
        )
        return json.dumps({
            "html": profile_text
        }) 

@server.route('/warning', methods=["POST"])
def anom_warning():
    if request.method == "POST":
        warning_text = render_template(
            "warning.html",
        )
        return json.dumps({
            "html": warning_text
        })    

@server.route('/about', methods=["POST"])
def about():
    if request.method == "POST":
        about_text = render_template(
            "about.html",
        )
        return json.dumps({
            "html": about_text
        })

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/Dash/'
)

app.layout = html.Div("My Dash app")

if __name__ == '__main__':
    app.run_server(debug=True)