from config.config import MySQL, APIKeys
import requests
import pandas as pd
from models.schemas import StaticBike
from datetime import datetime

def get_weather_forecast():
    url = f'http://api.openweathermap.org/data/2.5/forecast?' \
          f'q=Dublin,ie' \
          f'&appid={APIKeys.openweather_key}' \
          f'&units=metric'
    response = requests.get(url)
    response.raise_for_status()
    print("Bike Request=", response.request.url)
    print("Bike Response=", response.content)
    result = []
    if response:
        data = response.json()
        slot_data = {}
        for timeslot in data["list"]:
            slot_data['time'] = timeslot["dt"]
            slot_data['wind_speed'] = timeslot["wind"]["speed"]
            slot_data['temperature'] = timeslot["main"]["temp"]
            slot_data['pressure'] = timeslot["main"]["pressure"]
            slot_data['humidity'] = timeslot["main"]["humidity"]
            result.append(slot_data)
            slot_data = {}
    return result

def get_station_coordinate(db, station_num):
    station = db.session.query(StaticBike) \
        .filter(StaticBike.number == station_num).first()

    if station is None:
        return None, None
    else:
        return station.latitude, station.longitude

def create_prediction_input(weahter_data, latitude, longitude):
    rows = []
    column_name = ['latitude', 'longitude', 'temperature', 'wind_spd', 'pressure', 'humidity', 'hour',
     'weekday_Monday', 'weekday_Tuesday', 'weekday_Wednesday', 'weekday_Thursday', 'weekday_Friday',
     'weekday_Saturday', 'weekday_Sunday']
    slot_timestamps = []

    for slot_data in weahter_data:
        row = []
        for hour_interval in range(3):
            row.append(latitude)
            row.append(longitude)
            row.append(slot_data['temperature'])
            row.append(slot_data['wind_speed'])
            row.append(slot_data['pressure'])
            row.append(slot_data['humidity'])
            slot_timestamp = slot_data['time'] + (3600 * hour_interval)
            dt_obj = datetime.fromtimestamp(slot_timestamp)
            slot_timestamps.append(slot_timestamp)
            row.append(dt_obj.hour)
            for i in range(7):
                if i == dt_obj.weekday():
                    row.append(1)
                else:
                    row.append(0)
            rows.append(row)
            row = []

    return pd.DataFrame(rows, columns=column_name), slot_timestamps
