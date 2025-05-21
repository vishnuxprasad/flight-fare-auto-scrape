# Flight Fare Auto Scraper

**Flight Fare Auto Scraper** is a Python-based automation tool designed to extract flight pricing and schedule data from airline websites using [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/). It enables accurate and structured data collection, making it suitable for fare monitoring, travel research, and aviation data analysis workflows.
> **Note:** As of now, the tool supports **only one-way flight searches** on the **Emirates** website.

---

## Features

- Automated interaction with airline website
- One-way flight selection and date input automation
- Scroll automation to ensure complete data capture
- Exports results to a clean, structured `csv` file

---

## Project Structure

```
flight-fare-auto-scrape/
│
├── src/
│ └── farescraper/
│ ├── init.py
│ ├── emirates/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── config.py
│ │ ├── booking_page.py
│ │ ├── date_picker.py
│ │ ├── scraper.py
│ │ ├── utils.py
│
├── input.csv
├── results/
├── requirements.txt
├── setup.py
├── .gitignore
├── .env
└── README.md
```

---

## Requirements

- Python 3.7 or higher  
- Google Chrome browser  
- ChromeDriver (must match your Chrome version, see [documentation](https://developer.chrome.com/docs/chromedriver/downloads).)

## Recommended: Virtual Environment Setup

To isolate dependencies and avoid conflicts. [Read more](https://docs.python.org/3/library/venv.html).

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Installation
After activating your virtual environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

---

## Input Format

Edit `input.csv` with routes and travel dates using the format below:

```csv
from,to,date
DXB,LHR,25-06-2025
DEL,JFK,30-06-2025
```

- Date format: `DD-MM-YYYY`
- Valid range: from today up to 330 days ahead

---

## Configuration

In `.env`, set your local path to `chromedriver`:

```python
CHROME_DRIVER_PATH = "/path/to/chromedriver"
```

---

## Running the Scraper

This tool is designed to support multiple airline websites via dedicated modules.  
As of now, the scraper supports **Emirates** only.

To execute the Emirates scraper:

```bash
python -m farescraper.emirates
```


After successful execution, the scraped results will be saved to:

```
results/emirates_flights.csv
```

---

## Output Example

| From | To  | Departure         | Arrival           | Nonstop | No. of Connections | Price     |
|------|-----|-------------------|-------------------|---------|---------------------|-----------|
| Dubai  | London Heathrow | 09:00, 25-06-2025 | 13:30, 25-06-2025 | Yes     | 0                   | 1,230 AED |

---

## Limitations

- Currently supports only **one-way flight searches on the Emirates website**.
- The tool may require adjustments if the respective website’s layout, structure, or underlying `HTML` changes.
- Due to the wide range of possible booking scenarios and dynamic web behavior, some edge cases may not be fully accounted for in the current implementation.

---

## Contributing

Contributions are welcome. Please feel free to open issues or submit pull requests to improve functionality, add new features (e.g., round-trip or multi-city support), add more airline websites or enhance scraping robustness.
