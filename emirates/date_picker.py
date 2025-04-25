import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .utils import validate_date, month_to_number

class EmiratesDatePicker:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def pick(self, date_str: str):
        # Parse and validate target date
        target = validate_date(date_str)
        month = target.strftime("%B")
        year = target.year
        target_month_number = month_to_number[month]

        # Wait for calendar widget
        self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "div.SingleDatePicker_picker"
        )))

        # Locate navigation buttons
        prev_btn = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "button.DayPickerNavigation_leftButton__horizontal"
        )))
        next_btn = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "button.DayPickerNavigation_rightButton__horizontal"
        )))

        # Get currently visible months
        caps = self.wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.CalendarMonth[data-visible='true'] .CalendarMonth_caption strong"
        )))
        visible = []
        for el in caps:
            m_str, y_str = el.text.split()
            visible.append((month_to_number[m_str], int(y_str)))
        (m1, y1), _ = visible

        # Calculate month difference and navigate
        diff = (year - y1) * 12 + (target_month_number - m1)
        btn = next_btn if diff > 0 else prev_btn
        for _ in range(abs(diff)):
            btn.click()
            time.sleep(0.5)

        # Click target day
        xpath = (
            f"//div[@id='{month}_{year}']"
            "/parent::div/following-sibling::table"
            f"//td[@id='{date_str}']/a"
        )
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            self.wait.until(EC.invisibility_of_element_located((
                By.CSS_SELECTOR, "div.SingleDatePicker_picker"
            )))
        except TimeoutException:
            raise NoSuchElementException(f"Could not select date {date_str}")
