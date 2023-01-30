# html, csv, json files

import time
from bs4 import BeautifulSoup as bs


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("book_journey.html", "r") as f:
        journey_html = soup = bs(f, "html.parser")

def get_export_buttons_with_bs4() -> list:
    # section with the buttons to "Export Your Data" as CSV/HTML/JSON
    section = journey_html.find("div", class_ = "popover-choices popover-scroller native-scrollable native-scrollable-y popover-content halos-anchor")
    for export_item in ("Export Your Data", "Table", "CSV"):
        # All possible items (but would waste processing power): ("Export Your Data", "Table", "HTML", "Spreadsheet", "CSV", "Data", "JSON"):
        if not export_item in section.text:
            raise RuntimeError("In book \"" + journey_html.title.text + "\": Searching in the wrong place for HTML and CSV and JSON file export buttons.")


    # now it should be one of these:
    export_spans_html = section.find_all("span", class_ = "popover-choice-indicator") # okay
    export_buttons_html = section.find_all("a", class_ = "halo", attrs="role='button'") # okay

    return export_spans_html, export_buttons_html

def click_buttons_with_bs4():
    export_spans_html, export_buttons_html = get_export_buttons_with_bs4()
    for span in export_spans_html:
        print(span) # span.click()

    for button in export_buttons_html:
        button.click()

def get_export_buttons_with_selenium() -> list:
    # initializing webdriver for Chrome
    chrome_options = Options()
    user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile"
    chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # section with the buttons to "Export Your Data" as CSV/HTML/JSON
    export_urls = {}
    for export_type in ("Table", "Spreadsheet", "Data"):
        driver.get("https://libbyapp.com/timeline/activities/journey/1337141")
        try:
            actions_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='shelf-actions' and @type='button']"))
            )
            actions_button.click()
            time.sleep(3)

            menu_button_export = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='text' and text() = 'Export Reading Data']"))
            )
            menu_button_export.click()
            time.sleep(3)

            export_type_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@class='halo' and @role='button']/span[@role='text' and text() = '{export_type}']"))
            )
            export_type_button.click()
            time.sleep(3)

            print(driver.current_url)
            export_urls[export_type] = driver.current_url
            if export_type == "Spreadsheet":
                continue
        except:
            driver.quit()
            exit()

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "myDynamicElement"))
            )
        finally:
            driver.quit()
    print(export_urls)

    # .click() # "//span[@role='text'][text()='Export Reading Data'").click()
    # <span role="text">Export Reading Data</span>

    # section = Select(driver.find_element(By.XPATH, "//div[@class='popover-choices popover-scroller native-scrollable native-scrollable-y popover-content halos-anchor'][1]"))
    # section = Select()
    # print(section)
    # section.click()
    # # for export_item in ("Export Your Data", "Table", "CSV"):
    #     # All possible items (but would waste processing power): ("Export Your Data", "Table", "HTML", "Spreadsheet", "CSV", "Data", "JSON"):
    #     if not export_item in section.text:
    #         raise RuntimeError("In book \"" + journey_html.title.text + "\": Searching in the wrong place for HTML and CSV and JSON file export buttons.")


    # # now it should be one of these:
    # export_spans_html = section.find_all("span", class_ = "popover-choice-indicator") # okay
    # export_buttons_html = section.find_all("a", class_ = "halo", attrs="role='button'") # okay

get_export_buttons_with_selenium()