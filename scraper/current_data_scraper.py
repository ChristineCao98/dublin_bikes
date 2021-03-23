import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.schemas import Base, DublinBike
from config.config import MySQL, APIKeys
from scraper import current_weather_scraper
import pytz


def scrape():
    try:
        scrape_bike_and_weather()
    except Exception as e:
        print("Error: " + str(e))


def scrape_bike_and_weather():
    print('in scrape_bike_and_weather')
    engine = create_engine(MySQL.URI)
    Base.metadata.create_all(engine)  # Create table
    Session = sessionmaker(bind=engine)
    session = Session()

    api = "https://api.jcdecaux.com/vls/v1/stations"
    parameters = {'contract': 'dublin', 'apiKey': APIKeys.bike_API}

    response = requests.get(api, verify=True, params=parameters)

    response.raise_for_status()  # throw an error if made a bad request

    # print("Bike Request=", response.request.url)
    # print("Bike Response=", response.content)

    if response:
        response = response.json()
        utc_now = datetime.utcnow()
        dt = utc_now.strftime("%Y-%m-%d %H:%M:%S")
        current_weather_scraper.scrape(dt)

        # Build table with columns
        for row in response:
            scraping_time = dt
            number = row["number"]
            if row["last_update"]:
                last_update = datetime.fromtimestamp(row["last_update"] / 1000)
            else:
                last_update = None
            site_names = row["name"]
            address = row["address"]
            latitude = row["position"]['lat']
            longitude = row["position"]['lng']
            bike_stand = row["bike_stands"]
            available_bike_stand = row["available_bike_stands"]
            available_bike = row["available_bikes"]
            status = row["status"]
            banking = row["banking"]
            bonus = row["bonus"]
            localtime = pytz.utc.localize(utc_now) \
                .astimezone(pytz.timezone('Europe/Dublin'))
            session.add(DublinBike(scraping_time=scraping_time,
                                   number=number,
                                   last_update=last_update,
                                   site_names=site_names,
                                   address=address,
                                   latitude=latitude,
                                   longitude=longitude,
                                   bike_stand=bike_stand,
                                   available_bike_stand=available_bike_stand,
                                   available_bike=available_bike,
                                   status=status,
                                   banking=banking,
                                   bonus=bonus,
                                   localtime=localtime))

        session.commit()
        session.close()
        return dt


if __name__ == '__main__':
    scrape()
