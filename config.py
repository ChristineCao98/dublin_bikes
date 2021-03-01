import os

CONTRACT = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"


class APIKeys:
    openweather_key = os.getenv("WEATHER_API_KEY")
    bike_API = os.getenv("BIKE_API_KEY")


class MySQL:
    host = os.getenv("DB_URI")
    port = os.getenv("DB_PORT")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")
    URI = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
