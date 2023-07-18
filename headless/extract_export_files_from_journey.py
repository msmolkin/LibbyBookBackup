
# Purpose: Extract the HTML, CSV, and JSON files from the "Journey" page of a book in the Libby app.

# Claude's version:
# extract_export_files_from_journey.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_files(driver):

  # Navigate to page
  driver.get("https://libbyapp.com/timeline/activities/journey/1337141")

  while True:

    # Click export button
    actions_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='shelf-actions' and @type='button']"))
    )
    actions_button.click()

    menu_button_export = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@role='text' and text() = 'Export Reading Data']"))
    )
    menu_button_export.click()

    # export_type_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, f"//a[@class='halo' and @role='button']/span[@role='text' and text() = '{export_type}']"))
    # )

    # Get popover element
    popover = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".popover-choices"))
    )

    # Loop through each format
    for format in ["HTML", "CSV", "JSON"]:

      # Click button and get URL
      btn = popover.find_element(By.XPATH, f"//span[text()='{format}']/..")
      btn.click() 
      url = driver.current_url  

      print(f"{format} URL:", url)

      # Navigate back
      driver.back()

    # Check for Done button 
    if len(driver.find_elements(By.XPATH, "//span[text()='Done']")):
      break

if __name__ == "__main__":
    chrome_options = Options()
    user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile"
    chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    extract_files(driver)

# My version, riddled with errors:
# import time
# from bs4 import BeautifulSoup as bs


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def get_export_buttons_with_bs4(html_file: str) -> list:
#     """ Gets the buttons to export the data as HTML, CSV, and JSON files.

#     Raises:
#         RuntimeError: If the buttons are not found.

#     Returns:
#         list: The buttons to export the data as HTML, CSV, and JSON files.
#     """
    
#     # open the HTML file
#     with open(html_file, "r") as book_journey_html_file:
#         journey_html = soup = bs(book_journey_html_file.read(), "html.parser")
    
#     # section with the buttons to "Export Your Data" as CSV/HTML/JSON
#     section = journey_html.find("div", class_ = "popover-choices popover-scroller native-scrollable native-scrollable-y popover-content halos-anchor")

#     for export_item in ("Export Your Data", "Table", "CSV"):
#         # All possible items (but would waste processing power): ("Export Your Data", "Table", "HTML", "Spreadsheet", "CSV", "Data", "JSON"):
#         if not export_item in section.text:
#             raise RuntimeError("In book \"" + journey_html.title.text + "\": Searching in the wrong place for HTML and CSV or JSON file export button.")


#     # now it should be one of these:
#     export_spans_html = section.find_all("span", class_ = "popover-choice-indicator") # okay
#     export_buttons_html = section.find_all("a", class_ = "halo", attrs="role='button'") # okay

#     return export_spans_html, export_buttons_html

# def click_buttons_with_bs4():
#     """ Clicks the buttons to export the data as HTML, CSV, and JSON files.
#     """
#     book_journey_filename = "book_journey.html"
#     export_spans_html, export_buttons_html = get_export_buttons_with_bs4(book_journey_filename)
#     for span in export_spans_html:
#         print(span) # span.click()

#     for button in export_buttons_html:
#         button.click()

# def get_export_buttons_with_selenium() -> list:
#     # initializing webdriver for Chrome
#     chrome_options = Options()
#     user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile"
#     chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
#     # chrome_options.add_argument("--headless")
#     driver = webdriver.Chrome(options=chrome_options)

#     # section with the buttons to "Export Your Data" as CSV/HTML/JSON
#     export_urls = {}
#     for export_type in ("Table", "Spreadsheet", "Data"):
#         timeline_url = "https://libbyapp.com/timeline/activities/journey/1337141"
#         driver.get(timeline_url)
#         try:
#             actions_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[@class='shelf-actions' and @type='button']"))
#             )
#             actions_button.click()

#             menu_button_export = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, "//span[@role='text' and text() = 'Export Reading Data']"))
#             )
#             menu_button_export.click()

#             export_type_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, f"//a[@class='halo' and @role='button']/span[@role='text' and text() = '{export_type}']"))
#             )
#             export_type_button.click()
#             time.sleep(3)
#             print("export_type_button")

#             print(driver.current_url)
            
#             export_urls[export_type] = driver.current_url
#             if export_type == "Spreadsheet":
#                 export_urls["Spreadsheet"] = {
#                     "Circulation": driver.find_element(By.LINK_TEXT, "Circulation").get_attribute("href"),
#                     "Reading Journey": driver.find_element(By.LINK_TEXT, "Reading Journey").get_attribute("href")
#                 }
#                 print(export_urls["Spreadsheet"])
#             else:
#                 export_urls[export_type] = driver.current_url
#         except:
#             # driver.quit()
#             exit()
#     print(export_urls)

#     # .click() # "//span[@role='text'][text()='Export Reading Data'").click()
#     # <span role="text">Export Reading Data</span>

#     # section = Select(driver.find_element(By.XPATH, "//div[@class='popover-choices popover-scroller native-scrollable native-scrollable-y popover-content halos-anchor'][1]"))
#     # section = Select()
#     # print(section)
#     # section.click()
#     # # for export_item in ("Export Your Data", "Table", "CSV"):
#     #     # All possible items (but would waste processing power): ("Export Your Data", "Table", "HTML", "Spreadsheet", "CSV", "Data", "JSON"):
#     #     if not export_item in section.text:
#     #         raise RuntimeError("In book \"" + journey_html.title.text + "\": Searching in the wrong place for HTML and CSV and JSON file export buttons.")


#     # # now it should be one of these:
#     # export_spans_html = section.find_all("span", class_ = "popover-choice-indicator") # okay
#     # export_buttons_html = section.find_all("a", class_ = "halo", attrs="role='button'") # okay

# if __name__ == "__main__":
#     # get_export_buttons_with_selenium()
#     click_buttons_with_bs4()