from scraper import dublin_bike_data  # ,forecast_scraper
import time

def main():
    while True:
        try:
            print("Start Scraping...")
            stations = dublin_bike_data.scrape()
            print("End of Scraping...")
            time.sleep(5 * 60)
        except Exception as e:
            print("Error: " + str(e))
    print("End of scheduler")
main()

