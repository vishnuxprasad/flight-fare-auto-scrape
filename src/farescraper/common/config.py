import os
from dotenv import load_dotenv

load_dotenv()

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
if not CHROME_DRIVER_PATH:
    raise RuntimeError(
        "CHROME_DRIVER_PATH not set in .env file. Please set it to the path of your ChromeDriver."
    )
