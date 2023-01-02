# Extract the Title and Author and last edited date (or circulation date) from the following HTML:

# Had HTML of a page here for testing. Replaced with the local file.

# The output should be:
#   The Body Keeps the Score
#   Bessel van der Kolk, M.D.

import pathlib
from bs4 import BeautifulSoup as bs
from datetime import datetime

# Read the HTML from a file
html = pathlib.Path("book.html").read_text()

# Parse the HTML
soup = bs(html, "html.parser")
table_titleinfo = soup.find("table", class_="share-table-1d")

# Extract the title and author
title = table_titleinfo.find("a").text
author = table_titleinfo.find_all("td")[1].text

# Extract the last edited date
table_edits = soup.find("table", class_="share-table-2d")
date_latest_note = table_edits.find_all("td")[0].text

# Extract the circulation date
table_circulation = soup.find_all("table", class_="share-table-2d")[1]
date_latest_circulation_change = table_circulation.find_all("td")[0].text

# convert the date to a datetime object
date_latest_note = datetime.strptime(date_latest_note.strip(), "%B %d, %Y %H:%M")
date_latest_circulation_change = datetime.strptime(date_latest_circulation_change.strip(), "%B %d, %Y %H:%M")
last_edit_formatted_for_filename = max(date_latest_note, date_latest_circulation_change).strftime("%Y-%m-%d %H-%M")


print(last_edit_formatted_for_filename + " " + title + " by " + author + " book notes (downloaded " + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ")")