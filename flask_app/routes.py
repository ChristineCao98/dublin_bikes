from flask import Flask, render_template, jsonify, url_for
from models.schemas import DublinBike
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from sqlalchemy import func, extract
from config.config import MySQL, APIKeys
from time import time
import datetime
import pickle
import toolkits.prediction_helper as helper
from scraper.weather_forecast_scraper import scrape
from flask_apscheduler import APScheduler
from scraper import current_data_scraper as current_scraper
from flask_app import prediction_model_builder as ml_builder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = MySQL.URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
scheduler = APScheduler()

db = SQLAlchemy(app)
cache = Cache(app)


@app.route('/')
@cache.cached()
def index():
    return render_template('index.html', map_api=APIKeys.map_API, time=time)


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


@app.route('/api/weather/<int:station_id>')
@cache.cached(timeout=300)
def get_weather(station_id):
    """Return weather information of weather information of current day and the following 5 days"""
    latitude, longitude = helper.get_station_coordinate(db, station_id)
    return jsonify(scrape(latitude, longitude))


@app.route('/api/hour/<int:station_id>')
@cache.cached()
def get_hourly(station_id):
    """Return average hourly number of available bikes"""
    hourdata = db.session.query(func.avg(DublinBike.available_bike)) \
        .filter(DublinBike.number == station_id) \
        .group_by(extract('hour', DublinBike.localtime)) \
        .order_by(extract('hour', DublinBike.localtime)) \
        .all()
    return jsonify([
        {'hour': i,
         'available_bike': float(hourdata[i][0])
         } for i in range(24)
    ])


@app.route('/api/day/<int:station_id>')
@cache.cached()
def get_daily(station_id):
    """Return average daily number of available bikes"""
    dailydata = db.session.query(func.avg(DublinBike.available_bike)) \
        .filter(DublinBike.number == station_id) \
        .group_by(func.dayofweek(DublinBike.localtime)) \
        .order_by(func.dayofweek(DublinBike.localtime)) \
        .all()
    return jsonify([
        {'day': i,
         'available_bike': float(dailydata[i][0])
         } for i in range(7)
    ])


@app.route('/api/prediction/<int:station_id>')
@cache.cached()
def get_prediction(station_id):
    """Return the prediction data of available bikes in the following 5 days"""
    # load prediction model
    model = pickle.load(open(app.root_path + '\\bike_prediction_model.pickle', "rb"))

    latitude, longitude = helper.get_station_coordinate(db, station_id)
    if latitude and longitude:
        # prepare input data
        weather_data = helper.get_weather_forecast()
        input_x, slot_timestamps = helper.create_prediction_input(weather_data, latitude, longitude)
        slot_datetimes = [datetime.datetime.fromtimestamp(i) for i in slot_timestamps]

        # predict
        prediction_y = model.predict(input_x)

        # prepare for response object
        res_list = []
        day_list = []
        prev = slot_datetimes[0].day
        day_list.append({
            'date': slot_datetimes[0],
            'hour': slot_datetimes[0].hour,
            'available_bike': prediction_y[0]
        })
        for i in range(1, len(slot_datetimes)):
            if prev != slot_datetimes[i].day or i == len(slot_datetimes) - 1:
                prev = slot_datetimes[i].day
                res_list.append(day_list)
                day_list = []
            day_list.append({
                'date': slot_datetimes[i],
                'hour': slot_datetimes[i].hour,
                'available_bike': prediction_y[i]
            })
        return jsonify(res_list)
    else:
        return jsonify({})

def current_data_scraping_task():
    current_scraper.scrape()

def ml_building_task():
    ml_builder.build(app)


if __name__ == '__main__':
    hours = '4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0'
    minutes = '0,5,10,15,20,25,30,35,40,45,50,55'
    scheduler.add_job(id='current_data_scraper', func=current_data_scraping_task, trigger='cron', hour=hours, minute=minutes)
    scheduler.add_job(id='ml_builder', func=ml_building_task, trigger='cron', hour='1', minute='30')
    scheduler.start()
    app.run(debug=True, use_reloader=False)
