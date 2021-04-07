import requests
import datetime
from config.config import APIKeys


def scrape(lat, long):
    url = f'http://api.openweathermap.org/data/2.5/onecall?' \
          f'lat={lat}' \
          f'&lon={long}' \
          f'&appid={APIKeys.openweather_key}' \
          f'&units=metric'
    response = requests.get(url)
    response.raise_for_status()
    if response:
        data = response.json()
        ret = data['daily']
        if datetime.datetime.utcnow().day != data['daily'][0]:
            ret.pop(0)
            ret.insert(0, data['current'])
            ret[0]['temp'] = {'day': ret[0]['temp']}
        return ret
