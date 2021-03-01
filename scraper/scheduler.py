from scraper import dublin_bike_data  # ,forecast_scraper
import time

def main():
    while True:
        stations = dublin_bike_data.scrape()
        time.sleep(5 * 60)

main()

