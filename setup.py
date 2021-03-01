from setuptools import setup

setup(name="dublin-bike",
      version="0.1",
      description="Dublin Bike Availability Prediction",
      url="",
      author="AY",
      author_email="",
      licence="GPL3",
      packages=['scraper', 'models'],
      entry_points={
        'console_scripts':['bike_scraper=scraper.scheduler:main']
        }
      )
