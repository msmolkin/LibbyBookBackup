import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# initializing webdriver for Chrome
chrome_options = Options()
user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/michael/Library/Application Support/Google/Chrome/"
chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}", "--headless"])
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)


timeline_url = "https://libbyapp.com/timeline/activities"
years = [2023, 2022] # replace with datetime.datetime.year and year-1
months = [i + 1 for i in range(12)]

def open_all_months():
    for yyyy in years:
        for mm in months:
            driver.get(f"https://libbyapp.com/timeline/activities/all,all,all,{yyyy}-{mm}")
            # and do everything under here instead

def open_book():
    driver.get("https://libbyapp.com/timeline/activities/all,all,all,2022-12")
    # driver.get("https://www.yahoo.com/")
    time.sleep(3)
    # driver.get_screenshot_as_png()
    driver.save_screenshot("screenshot.png")

open_book()

# closing browser
driver.close()
