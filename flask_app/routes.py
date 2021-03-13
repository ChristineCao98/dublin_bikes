from flask import Flask, render_template, jsonify, url_for
from models.schemas import DublinBike
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from sqlalchemy import func
from config.config import MySQL, APIKeys
from time import time
import pickle
import pandas as pd
import toolkits.prediction_helper as helper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = MySQL.URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

db = SQLAlchemy(app)
cache = Cache(app)


@app.route('/')
@cache.cached()
def index():
    return render_template('index.html', map_api=APIKeys.map_API,time=time)


@app.route('/api/stations/')
@cache.cached()
def get_all_stations():
    """Return details of all stations"""
    latest_scraping_time = db.session \
        .query(func.max(DublinBike.scraping_time)) \
        .one()[0]

    stations = db.session.query(DublinBike) \
        .filter(DublinBike.scraping_time == latest_scraping_time) \
        .order_by(DublinBike.number.asc()) \
        .all()

    return jsonify({
        'data': [station.serialize for station in stations]
    })


@app.route('/api/stations/<int:station_id>')
@cache.cached()
def get_station(station_id):
    """Return details of the station"""
    station = db.session.query(DublinBike) \
        .filter(DublinBike.number == station_id) \
        .order_by(DublinBike.scraping_time.desc()) \
        .first()

    return jsonify({
        'data': station.serialize
    })


@app.route('/api/prediction/<int:station_id>')
@cache.cached()
def get_prediction(station_id):

    model = pickle.load(open('bike_prediction_model.pickle', "rb"))

    latitude, longitude = helper.get_station_coordinate(db, station_id)
    if latitude and longitude:
        weather_data = helper.get_weather_forecast()
        input_x, slot_timestamps = helper.create_prediction_input(weather_data, latitude, longitude)
        prediction = model.predict(input_x)
        prediction_list = [int(i) for i in prediction.tolist()]

        return jsonify({
            'timestamp': slot_timestamps,
            'availability_prediction': prediction_list
        })
    else:
        return jsonify({})



if __name__ == '__main__':
    app.run(debug=True)
