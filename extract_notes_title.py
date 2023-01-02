# Extract the Title and Author from from the following HTML:

# Had HTML of a page here for testing. Replaced with the local file.


# The output should be:
#   The Body Keeps the Score
#   Bessel van der Kolk, M.D.

from bs4 import BeautifulSoup as bs
import pathlib

# Read the HTML from a file
html = pathlib.Path("book.html").read_text()

# Parse the HTML
soup = bs(html, "html.parser")
table = soup.find("table", class_="share-table-1d")

# Extract the title and author
title = table.find("a").text
author = table.find_all("td")[1].text

print(title + " by " + author + " book notes")