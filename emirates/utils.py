from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

month_to_number = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def validate_date(date_str: str, max_days: int = 330) -> date:
    """
    Parse 'DD-MM-YYYY', ensure today ≤ date ≤ today + max_days.
    Returns a datetime.date on success, raises ValueError otherwise.
    """
    try:
        tgt = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        raise ValueError(f"Invalid format or invalid date: {date_str!r}. Expected format is DD-MM-YYYY.")

    today = date.today()
    if tgt < today:
        raise ValueError(f"Date {date_str} is in the past")
    if tgt > today + timedelta(days=max_days):
        raise ValueError(
            f"Date {date_str} is beyond {max_days}-days window from today."
        )
    return tgt


def create_driver(executable_path: str, detach: bool = True):
    """
    Spins up a Chrome WebDriver with required options.
    """
    service = Service(executable_path)
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", detach)
    return webdriver.Chrome(service=service, options=opts)
