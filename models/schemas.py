from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime

Base = declarative_base()


class DublinBike(Base):
    __tablename__ = 'bike_history'
    scraping_time = Column(String(32), primary_key=True)
    number = Column(Integer, primary_key=True)
    last_update = Column(String(32))
    address = Column(String(64))
    site_names = Column(String(64))
    latitude = Column(Float)
    longitude = Column(Float)
    bike_stand = Column(Integer)
    available_bike_stand = Column(Integer)
    available_bike = Column(Integer)
    status = Column(String(16))
    banking = Column(Boolean)
    bonus = Column(Boolean)
    localtime = Column(DateTime)

    @property
    def serialize(self):
        return {
            'scraping_time': self.scraping_time,
            'number': self.number,
            'last_update': self.last_update,
            'address': self.address,
            'site_names': self.site_names,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'bike_stand': self.bike_stand,
            'available_bike_stand': self.available_bike_stand,
            'available_bike': self.available_bike,
            'status': self.status,
            'banking': self.banking,
            'bonus': self.bonus
        }


class CurrentWeather(Base):
    __tablename__ = 'weather_history'
    stationNum = Column(Integer, primary_key=True)
    datetime = Column(DateTime(30), primary_key=True, nullable=False)
    temperature = Column(String(30), nullable=False)
    icon = Column(String(30))
    lon = Column(Float(30))
    lat = Column(Float(30))
    wind_spd = Column(Float(30))
    clouds = Column(Float(30))
    sunset = Column(String(30))
    sunrise = Column(String(30))
    pressure = Column(String(30))
    humidity = Column(String(30))
    code = Column(String(30))
    weekday = Column(Integer)

    def __init__(self, stationNum, datetime, lon, lat, temperature, wind_spd,
                 clouds, sunrise, sunset, pressure, humidity, code, icon, weekday):
        self.stationNum = stationNum
        self.datetime = datetime
        self.lon = lon
        self.lat = lat
        self.temperature = temperature
        self.wind_spd = wind_spd
        self.clouds = clouds
        self.sunrise = sunrise
        self.sunset = sunset
        self.pressure = pressure
        self.humidity = humidity
        self.code = code
        self.icon = icon
        self.weekday = weekday

    @property
    def serialize(self):
        return {
            'datetime': self.datetime,
            'lon': self.lon,
            'lat': self.lat,
            'temperature': self.temperature,
            'wind_spd': self.wind_spd,
            'clouds': self.clouds,
            'sunset': self.sunset,
            'description': self.description,
            'code': self.code,
            'icon': self.icon,
            'weekday': self.weekday
        }


class StaticBike(Base):
    __tablename__ = 'static_bike'
    __table_args__ = {'sqlite_autoincrement': True}
    number = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64))
    address = Column(String(64))
    latitude = Column(Float)
    longitude = Column(Float)

    @property
    def serialize(self):
        return {
            'number': self.number,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
