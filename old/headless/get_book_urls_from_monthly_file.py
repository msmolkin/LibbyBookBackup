# called inside open_libby_in_headless_chrome.py to get
# the following data for every book on the page: URL, is it a book or audiobook, book title

import re
from bs4 import BeautifulSoup as bs


def read_activities_file_and_extract_books() -> list:
    """ Creates list of books that had records in the current month


    Returns:
        books {list}: the books recorded so far
    """
    books = {}  # uses dict to save each book once
    with open("month_activities.html", "r") as f:
        soup = bs(f, "html.parser")

    books_on_this_page = soup(class_="title-plank-details")
    print(len(books_on_this_page)) # all books on the page
    base = "https://libbyapp.com"

    for book_html in books_on_this_page:
        book = {}

        book["url"] = base + book_html.find("a", class_="title-plank-journey")["href"]
        
        book["id"] = book["url"][book["url"].rindex("/") + 1:]

        tpa_aria_label = book_html.find("a", class_="title-plank-action").attrs["aria-label"]
        book["type"] = tpa_aria_label[:tpa_aria_label.index(":")]
        
        book["title"] = book_html("a")[0].find("span", class_ = "title-plank-title").text
        book["title"] = re.sub("&nbsp;|\xa0", " ", book["title"])
        book["title"] = re.sub("'|\"|\?", "", book["title"])

        book["author"] = book_html.find(class_="title-plank-author").text

        books[book["id"]] = book
    print(len(books)) # all books recorded (excluding duplicates)
    return books

def append_to_books_json(books: list) -> None:
    """ Appends new books to books.json

    Args:
        books (list): the books recorded so far
    """
    import json
    books_json = {}

    try:
        with open("books.json", "r") as f:
            books_json = json.load(f)
    except FileNotFoundError:
        pass
    
    for book_id in books:
        books_json[book_id] = books[book_id]
    with open("books.json", "w") as f:
        json.dump(books_json, f, indent=4)

if __name__ == "__main__":
    # time how long it takes to extract books from a file
    import time
    start_time = time.time()
    books = read_activities_file_and_extract_books()
    print("--- %s seconds ---" % (time.time() - start_time))
    # why is it so slow? 8 books per second

    # the books dict is saved?/stored?/sorted?/recorded?/filed? by book id: {book id: {book data}}
    # for book_id in books:
    #     assert(book_id == books[book_id]["id"])
    
    # from pprint import pprint
    # pprint(books)
    # print(len(books))