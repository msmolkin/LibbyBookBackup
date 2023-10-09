import json
import time
from datetime import datetime
from dateutil import relativedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import get_book_urls_from_monthly_file

TIMELINE_BASE_URL = "https://libbyapp.com/timeline/activities/"

def create_all_months() -> list:
    """ Creates a list of all months from today to 12 months ago

    Returns:
    res {list}: ["2021-10", "2021-09", ...]
    """
    today = datetime.today()
    res = []
    month_count = 0
    for month_count in range(12 + 1):
        date_month = today - relativedelta.relativedelta(months=month_count)
        res.append(date_month.strftime("%Y-%m"))
    return res

def save_file(file_name: str, html: str):
    """ Saves HTML webpage to file

    Takes a file name and html string as parameters and saves the html string to the file.

    Args:
    file_name {str}: name of file
    html {str}: webpage HTML
    """

    with open(file_name, "a") as f:
        f.write(html)

def open_timeline():
    """ Opens timeline and saves all months to file

    Copilot: Opens timeline and saves all months to file. Then calls get_book_urls_from_monthly_file.read_activities_file_and_extract_books() to extract all books from the HTML files.
    
    Text-davinci-003: Opens the timeline page for each month in the list created by create_all_months() and saves the page source to a file. It then calls the read_activities_file_and_extract_books() function from the get_book_urls_from_monthly_file module to extract the journey urls from the page source and save them to a json file.
    """

    months = create_all_months()
    for year_month in months:
        timeline_url = f"{TIMELINE_BASE_URL}all,all,all,{year_month}"
        driver.get(timeline_url)
        time.sleep(3)
        filename = "month_activities.html"
        save_file(filename, driver.page_source)

        get_book_urls_from_monthly_file.read_activities_file_and_extract_books()
    print(get_book_urls_from_monthly_file.books)
    with open("all_books_activities.json", "w") as list_of_books:
        json.dump(get_book_urls_from_monthly_file.books, list_of_books)


# not used. see get_book_urls_from_monthly_file.py
def open_book(book) -> object:
    """ Creates data for book
    book {str}: URL

    Returns:
    book_data {dict}: {url, book_type, title}
    """
    driver.get(book)
    time.sleep(3)
    book_data = {}
    book_data["url"] = book
    book_data["book_type"] = driver.find_element_by_class_name("book-type").text
    book_data["title"] = driver.find_element_by_class_name("book-title").text

    return book

if __name__ == "__main__":
    # initialize webdriver for Chrome

    chrome_options = Options()
    user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/$USER/Library/Application Support/Google/Chrome/LibbyProfile"
    chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    open_timeline()

    # Note: if "activities/journey" not in URL, then there was a problem with this book
    # https://libbyapp.com/timeline/activities/journey/82669

    # closing browser
    driver.close()