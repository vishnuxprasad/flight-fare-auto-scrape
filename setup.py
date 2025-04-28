from setuptools import setup, find_packages

setup(
    name="farescraper",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "selenium",
        "python-dotenv",
        "pandas",
    ],
    # entry_points={
    #     "console_scripts": [
    #         "scrape-emirates = farescraper.emirates:main",
    #     ],
    # },
)
