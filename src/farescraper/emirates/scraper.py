import time
import pandas as pd
import re
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class EmiratesFlightScraper:
    def __init__(self, driver):
        self.driver = driver
        self.flight_data = []

    def scroll_to_load_all(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_flight_data(self):
        self.scroll_to_load_all()

        cards = self.driver.find_elements(
            By.CLASS_NAME, "flight-card-cabin-price__wrapper"
        )
        for card in cards:
            try:
                depart_date = card.find_element(
                    By.CSS_SELECTOR,
                    ".flight-info__date-time-details.left p:nth-child(1)",
                ).text
                depart_time = card.find_element(
                    By.CSS_SELECTOR,
                    ".flight-info__date-time-details.left p:nth-child(2)",
                ).text
                arrive_date = card.find_element(
                    By.CSS_SELECTOR,
                    ".flight-info__date-time-details.right p:nth-child(1)",
                ).text
                arrive_time = card.find_element(
                    By.CSS_SELECTOR,
                    ".flight-info__date-time-details.right p:nth-child(2)",
                ).text
                depart_city = card.find_element(
                    By.CSS_SELECTOR,
                    ".flight-info__location.left .flight-info__location__shortname",
                ).text
                arrive_city = card.find_element(
                    By.CSS_SELECTOR,
                    ".flight-info__location.right .flight-info__location__shortname",
                ).text
                duration = card.find_element(
                    By.CLASS_NAME, "flight-info__infographic__duration"
                ).text
                price = card.find_element(By.CLASS_NAME, "currency-cash__amount").text
                currency = card.find_element(By.CLASS_NAME, "currency-cash__code").text

                # Default values
                nonstop = False
                connections = None

                # Check for non-stop button
                try:
                    card.find_element(
                        By.CLASS_NAME, "flight-info__infographic__nonstop-cta"
                    )
                    nonstop = True
                    connections = 0
                except NoSuchElementException:
                    # Try to find connection info
                    try:
                        connection_btn = card.find_element(
                            By.CLASS_NAME, "flight-info__infographic__stop-cta"
                        )
                        text = connection_btn.text.strip().lower()

                        # Only match number of connections
                        match = re.search(r"(\d+)\s+connection", text)
                        if match:
                            connections = int(match.group(1))
                            nonstop = False
                        else:
                            connections = None
                            nonstop = False
                    except NoSuchElementException:
                        connections = None
                        nonstop = None

                self.flight_data.append(
                    {
                        "From": depart_city,
                        "To": arrive_city,
                        "Departure": f"{depart_time}, {depart_date}",
                        "Arrival": f"{arrive_time}, {arrive_date}",
                        "Nonstop": "Yes"
                        if nonstop
                        else "No"
                        if nonstop is False
                        else "Unknown",
                        "No. of Connections": connections
                        if connections is not None
                        else "Unknown",
                        "Price": f"{price} {currency}",
                    }
                )
            except NoSuchElementException as e:
                print("Skipping a card due to missing info:", e)

    def to_csv(self, filename="results/emirates_flights.csv"):
        os.makedirs("results", exist_ok=True)
        df = pd.DataFrame(self.flight_data)
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} records to {filename}")
