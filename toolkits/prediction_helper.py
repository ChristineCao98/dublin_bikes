from config.config import MySQL, APIKeys
import datetime
import requests

def get_weather_forecast():
    url = f'http://api.openweathermap.org/data/2.5/forecast?' \
          f'q=Dublin,ie'\
          f'&appid={APIKeys.openweather_key}' \
          f'&units=metric'
    response = requests.get(url)
    response.raise_for_status()
    print("Bike Request=", response.request.url)
    print("Bike Response=", response.content)

    if response:
        data = response.json()
        for timeslot in data["list"]:
            wind_speed = timeslot["wind"]["speed"]
            temp = timeslot["main"]["temp"]
            pressure = timeslot["main"]["pressure"]
            humidity = timeslot["main"]["humidity"]

        print(wind_speed, ",", temp, ",", pressure)
        # dtObj = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        # weekday = dtObj.isoweekday()