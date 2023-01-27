# called inside open_libby_in_headless_chrome.py to get
# to get the data for every book on the page: URL, is it a book or audiobook, book title
# for (book of $$("a.title-plank-action.halo")) {
#     console.log(book.href, book.ariaLabel.slice(0, book.ariaLabel.indexOf(":")), book.firstChild.innerText)
# }

from pprint import pprint
from bs4 import BeautifulSoup as bs

with open("webpage.html", "r") as f:
    soup = bs(f, "html.parser")

all_books = soup(class_="title-plank-details")

# print(all_books)

for book in all_books:
    a = book("a")
    # print(a[0])
    url = book("a[href]")

    tpa_aria_label = book.find("a", "title-plank-action").attrs["aria-label"]
    book_type = tpa_aria_label[:tpa_aria_label.index(":")]  # book.ariaLabel.slice(0, book.ariaLabel.indexOf(":"))
    
    book_title = a[0].find("span", class_ = "title-plank-title").text
    # console.log(book.href, book.ariaLabel.slice(0, book.ariaLabel.indexOf(":")), book.firstChild.innerText)
    exit()