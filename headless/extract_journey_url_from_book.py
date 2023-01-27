# called inside open_libby_in_headless_chrome.py to get
# the following data for every book on the page: URL, is it a book or audiobook, book title

import re
from bs4 import BeautifulSoup as bs

books = {}  # uses dict to save each book once

def read_activities_file_and_extract_books() -> list:
    """ Creates list of books that had records in the current month


    Returns:
        books {list}: the books recorded so far
    """
    with open("month_activities.html", "r") as f:
        soup = bs(f, "html.parser")

    books_on_this_page = soup(class_="title-plank-details")

    for book_html in books_on_this_page:
        book = {}

        base = "https://libbyapp.com"
        book["url"] = base + book_html.find("a", class_="title-plank-journey")["href"]

        tpa_aria_label = book_html.find("a", class_="title-plank-action").attrs["aria-label"]
        book["type"] = tpa_aria_label[:tpa_aria_label.index(":")]  # book.ariaLabel.slice(0, book.ariaLabel.indexOf(":"))
        
        book["title"] = book_html("a")[0].find("span", class_ = "title-plank-title").text
        book["title"] = re.sub("&nbsp;|\xa0", " ", book["title"])
        book["title"] = re.sub("'|\"|\?", "", book["title"])

        book["author"] = book_html.find(class_="title-plank-author").text

        # I could pull the ID a bit cleaner from img[data-cover-slug="{book_id}"], but this is easier to code:
        book["id"] = book["url"][book["url"].rindex("/") + 1:]

        books[book["id"]] = book

        return books

# pprint(books)
# print(len(books))

if __name__ == "__main__":
    # test
    read_activities_file_and_extract_books()