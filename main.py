
from flask import Flask, request, render_template, url_for
from requests import get
from sys import argv


server = Flask(__name__)


@server.route("/")
def index():
    client = request.remote_addr
    if client.startswith(("192.164.", "10.", "100.", "172.", "192.0.", "198.18.")):
        you = get("https://4.ident.me").text
        ypayload = {"ip" : you};del you
        location = get("http://ip-api.com/json/", params = ypayload).json();del ypayload
    else:
        cpayload = {"ip" : client};del client
        location = get("http://ip-api.com/json/", params = cpayload).json();del cpayload

    usesFahr = ["US", "AS", "KY", "GU", "LR", "MH", "FM", "MP", "PW", "PR", "VI"]
    if location["countryCode"] in usesFahr:
        unitsDesired = "imperial"
        shortUnit = 'F'
    else:
        unitsDesired = "metric"
        shortUnit = 'C'
    del usesFahr

    wpayload = {
                    "appid" : argv[1], # API Key from OpenWeatherMap
                    "lat" : location['lat'], "lon" : location['lon'],
                    "units": unitsDesired
            }
    weather = get("https://api.openweathermap.org/data/2.5/weather", params = wpayload).json();del wpayload


    return render_template("index.html", location = location, weather = weather, shortUnit = shortUnit)


if __name__ == "__main__":
    server.run("0.0.0.0", 1984)


