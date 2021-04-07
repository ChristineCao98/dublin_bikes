import requests
import datetime
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from models.schemas import Base, CurrentWeather, StaticBike
from config.config import MySQL, APIKeys


def scrape(dt, app):
    app.logger.info("Scraping current weather")
    engine = create_engine(MySQL.URI)
    Base.metadata.create_all(engine)  # Create table
    Session = sessionmaker(bind=engine)
    session = Session()

    # fetch all stations data from database
    stations = session.query(StaticBike)

    if stations:

        for station in stations:

            url = f'http://api.openweathermap.org/data/2.5/weather?' \
                  f'lat={station.latitude}' \
                  f'&lon={station.longitude}' \
                  f'&appid={APIKeys.openweather_key}' \
                  f'&units=metric'

            response = requests.get(url)
            response.raise_for_status()

            app.logger.info("Weather Request=" + str(response.request.url))
            app.logger.info("Weather Response=" + str(response.content))

            if response:
                data = response.json()
                weather = data["weather"][0]
                temp = data["main"]["temp"]
                icon = weather["icon"]
                lon = data["coord"]["lon"]
                lat = data["coord"]["lat"]
                wind_spd = data["wind"]["speed"]
                clouds = data["clouds"]["all"]
                sunset = data["sys"]["sunset"]
                sunrise = data["sys"]["sunrise"]
                pressure = data["main"]["pressure"]
                humidity = data["main"]["humidity"]
                code = weather["id"]

                dtObj = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                weekday = dtObj.isoweekday()

                isDateTimeExist = session\
                    .query(exists()
                           .where(CurrentWeather.datetime
                                  == dtObj)
                           .where(CurrentWeather.stationNum
                                  == station.number))\
                    .scalar()

                # Only add to DB if the datetime(key) is not exist
                if not isDateTimeExist:
                    session.add(CurrentWeather(station.number, dtObj,
                                               lon, lat, temp, wind_spd,
                                               clouds, sunset, sunset, pressure, humidity,
                                               code, icon, weekday))
                    session.commit()

    else:
        app.logger.info("Can not find stations")
    session.close()
