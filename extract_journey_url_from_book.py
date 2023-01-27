# called inside open_libby_in_headless_chrome.py to get
# to get the data for every book on the page: URL, is it a book or audiobook, book title
# for (book of $$("a.title-plank-action.halo")) {
#     console.log(book.href, book.ariaLabel.slice(0, book.ariaLabel.indexOf(":")), book.firstChild.innerText)
# }

from pprint import pprint
import re
from bs4 import BeautifulSoup as bs

with open("webpage.html", "r") as f:
    soup = bs(f, "html.parser")

all_books = soup(class_="title-plank-details")
books = []

for book_html in all_books:
    book = {}

    base = "https://libbyapp.com"
    book["url"] = base + book_html.find("a", "title-plank-journey")["href"]

    tpa_aria_label = book_html.find("a", "title-plank-action").attrs["aria-label"]
    book["type"] = tpa_aria_label[:tpa_aria_label.index(":")]  # book.ariaLabel.slice(0, book.ariaLabel.indexOf(":"))
    
    book["title"] = book_html("a")[0].find("span", class_ = "title-plank-title").text
    book["title"] = re.sub("&nbsp;|\xa0", " ", book["title"])
    book["title"] = re.sub("'|\"|\p?", "", book["title"])

    # I could pull the ID from div[class="cover-box-clip"], img[data-cover-slug="63301"], but this easier
    book["id"] = book["url"][book["url"].rindex("/") + 1:]

    books.append(book)
    # books[book["id"]] = book

pprint(books)
print(len(books))