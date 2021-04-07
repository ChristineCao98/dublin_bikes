from scraper import current_data_scraper  # ,forecast_scraper
import time

''' To be deleted '''


def main():
    while True:
        try:
            print("Start Scraping...")
            stations = current_data_scraper.scrape()
            print("End of Scraping...")
            time.sleep(5 * 60)
        except Exception as e:
            print("Error: " + str(e))
    print("End of scheduler")


main()
