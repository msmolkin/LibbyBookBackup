# html, csv, json files

from bs4 import BeautifulSoup as bs

with open("book_journey.html", "r") as f:
        journey_html = soup = bs(f, "html.parser")
        
# tpa_aria_label = book_html.find("a", class_="title-plank-action").attrs["aria-label"]

# section with the "Export Your Data" as CSV/HTML/JSON buttons
section = journey_html.find("div", class_="popover-choices popover-scroller native-scrollable native-scrollable-y popover-content halos-anchor")
for export_item in ("Export Your Data", "Table", "CSV"):
    # All possible items (but would waste processing power): ("Export Your Data", "Table", "HTML", "Spreadsheet", "CSV", "Data", "JSON"):
    if not export_item in section.text:
        raise RuntimeError("In book \"" + journey_html.title.text + "\": Searching in the wrong place for HTML and CSV and JSON file export buttons.")


popover_buttons = journey_html.find_all("button", class_="popover-back-button halo")
spans = journey_html.find_all("span", class_="popover-back-button halo")
# <span role="text">Export Your Data</span><span id="shibui-element-0001" data-access="spoken" role="text">Back to previous popover.</span></div></button><a href="#" class="halo" role="button"><span role="text">Table</span><span class="popover-choice-indicator"><span role="text">HTML</span></span></a><a href="#" class="halo" role="button"><span role="text">Spreadsheet</span><span class="popover-choice-indicator"><span role="text">CSV</span></span></a><a href="#" class="halo" role="button"><span role="text">Data</span><span class="popover-choice-indicator"><span role="text">JSON</span></span></a></div></div></div><button class="shibui-shield halo" role="button" type="button" data-halo-class="shield" data-halo-inset="-1" aria-label="Close popover.">

export_links_html = [button for button in popover_buttons if button.attrs["aria-label"] == "Export Your Data"]
export_links_html = [span for span in popover_buttons if span.attrs["aria-label"] == "Export Your Data"]

print(export_links_html[0].text)

# tpa_aria_label = book_html.find("a", class_="title-plank-action").attrs["aria-label"]