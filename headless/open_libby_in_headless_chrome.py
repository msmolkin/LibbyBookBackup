import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import extract_journey_url_from_book

# initializing webdriver for Chrome
chrome_options = Options()
user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile"
chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


timeline_url = "https://libbyapp.com/timeline/activities"
years = [2023, 2022] # replace with datetime.datetime.year and year-1.
# maybe even just use last 12 months, if that's how they store it
months = [i + 1 for i in range(12)]

def open_all_months():
    for yyyy in years:
        for mm in months:
            driver.get(f"https://libbyapp.com/timeline/activities/all,all,all,{yyyy}-{mm}")
            # and do everything under here instead

def save_file(file_name: str, html: str):
    with open(file_name, "a") as f:
        f.write(html)

def open_timeline():
    driver.get("https://libbyapp.com/timeline/activities/all,all,all,2022-12")
    time.sleep(3)
    filename = "activities.html"
    save_file(filename, driver.page_source)

    print(extract_journey_url_from_book.books)

    """ Creates data for book
    book {str}: URL

    Returns:
    book_data {dict}: {url, book_type, title}
    """
def open_book(book) -> object:
    return book

open_timeline()

# Note: if "activities/journey" not in URL, then there was a problem with this book
# https://libbyapp.com/timeline/activities/journey/82669

# closing browser
driver.close()
