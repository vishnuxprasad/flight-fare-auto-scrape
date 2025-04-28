import pandas as pd
from farescraper.emirates import *

def main():
    # Load input data
    df = pd.read_csv("input.csv")

    # Initialize browser and page elements
    driver = create_driver(CHROME_DRIVER_PATH)
    page = EmiratesBookingPage(driver)
    picker = EmiratesDatePicker(driver)
    scraper = EmiratesFlightScraper(driver)

    for _, row in df.iterrows():
        origin = row["from"]
        destination = row["to"]
        travel_date = row["date"]

        # Navigate to booking page
        page.load()
        page.accept_cookies()
        page.select_one_way()

        # Set flight details
        page.enter_departure(origin)
        page.enter_arrival(destination)

        # Set date and search
        page.open_date_picker()
        picker.pick(travel_date)
        page.click_search_flights()

        # Scrape results
        scraper.extract_flight_data()

    # Save results
    scraper.to_csv()
    page.quit()

if __name__ == "__main__":
    main()
