import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class EmiratesBookingPage:
    URL = "https://www.emirates.com/english/book/"

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.cookies_accepted = False

    def load(self):
        # Open Emirates booking page
        self.driver.get(self.URL)

    def accept_cookies(self):
        # Accept cookies if not already done
        if self.cookies_accepted:
            return
        try:
            btn = self.wait.until(EC.element_to_be_clickable((
                By.ID, "onetrust-accept-btn-handler"
            )))
            btn.click()
            self.cookies_accepted = True
        except TimeoutException:
            pass

    def select_one_way(self):
        # Select "One way" option
        btn = self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//ul[@class='rsw-journey-tabs']//button[text()='One way']"
        )))
        btn.click()

    def enter_departure(self, code: str):
        # Enter departure airport code
        inp = self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//label[text()='Departure airport']/preceding-sibling::span//input"
        )))
        inp.send_keys(Keys.CONTROL + "a", Keys.DELETE, code, Keys.RETURN)
        time.sleep(1)
        inp.send_keys(code, Keys.RETURN)
        time.sleep(1)

    def enter_arrival(self, code: str):
        # Enter arrival airport code
        inp = self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//label[text()='Arrival airport']/preceding-sibling::span//input"
        )))
        inp.send_keys(code, Keys.RETURN)
        time.sleep(1)

    def open_date_picker(self):
        # Open calendar input
        picker_input = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            ".rsw-airports-calender__calender"
        )))
        picker_input.click()

    def click_search_flights(self):
        # Click search button
        btn = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div.responsive-search-widget__submit-button button"
        )))
        btn.click()

    def quit(self):
        # Close browser
        self.driver.quit()
