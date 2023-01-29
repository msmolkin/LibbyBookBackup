# html, csv, json files

from bs4 import BeautifulSoup as bs

with open("book_journey.html", "r") as f:
        journey_html = soup = bs(f, "html.parser")
        
# tpa_aria_label = book_html.find("a", class_="title-plank-action").attrs["aria-label"]

# section with the "Export Your Data" as CSV/HTML/JSON buttons
section = journey_html.find("div", class_ = "popover-choices popover-scroller native-scrollable native-scrollable-y popover-content halos-anchor")
for export_item in ("Export Your Data", "Table", "CSV"):
    # All possible items (but would waste processing power): ("Export Your Data", "Table", "HTML", "Spreadsheet", "CSV", "Data", "JSON"):
    if not export_item in section.text:
        raise RuntimeError("In book \"" + journey_html.title.text + "\": Searching in the wrong place for HTML and CSV and JSON file export buttons.")


# now it should be one of these:
export_spans_html = section.find_all("span", class_ = "popover-choice-indicator") # okay
export_buttons_html = section.find_all("a", class_ = "halo", attrs="role='button'") # okay

# for span in export_spans_html:
#     print(span) # span.click()

# for button in export_buttons_html:
#     button.click()

# tpa_aria_label = book_html.find("a", class_="title-plank-action").attrs["aria-label"]