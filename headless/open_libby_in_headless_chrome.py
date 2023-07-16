from datetime import datetime
from dateutil import relativedelta
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


timeline_base_url = "https://libbyapp.com/timeline/activities/"

def create_all_months() -> list:
    today = datetime.today()
    res = []
    month_count = 0
    for month_count in range(12 + 1):
        date_month = today - relativedelta.relativedelta(months=month_count)
        res.append(date_month.strftime("%Y-%m"))
    return res

def save_file(file_name: str, html: str):
    with open(file_name, "a") as f:
        f.write(html)

def open_timeline():
    months = create_all_months()
    for year_month in months:
        timeline_url = f"{timeline_base_url}all,all,all,{year_month}"
        driver.get(timeline_url)
        time.sleep(3)
        filename = "month_activities.html"
        save_file(filename, driver.page_source)

        extract_journey_url_from_book.read_activities_file_and_extract_books()
    print(extract_journey_url_from_book.books)
    with open("all_books_activities.html", "w") as list_of_books:
        list_of_books.write(extract_journey_url_from_book.books)


def open_book(book) -> object:
    """ Creates data for book
    book {str}: URL

    Returns:
    book_data {dict}: {url, book_type, title}
    """
    return book

open_timeline()

# Note: if "activities/journey" not in URL, then there was a problem with this book
# https://libbyapp.com/timeline/activities/journey/82669

# closing browser
driver.close()
