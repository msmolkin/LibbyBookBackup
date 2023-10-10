import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def export_timeline():
    # Initialize WebDriver
    chrome_options = Options()
    user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/michael/Library/Application Support/Google/Chrome/LibbyProfile"
    chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
    driver = webdriver.Chrome(options=chrome_options)

    # Set viewport size to the size I had when I first wrote this script
    # driver.set_window_size(543, 978)

    # Navigate to website
    driver.get("https://libbyapp.com/timeline/activities")

    # Wait for the Actions button
    wait = WebDriverWait(driver, 5)  # 5 seconds timeout
    actions_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#shelf-actions-pill-0001 > span')))
    actions_button.click()

    # Click Export Timeline
    export_timeline_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.arena-overlay a:nth-of-type(2)')))
    export_timeline_button.click()

    # Click JSON Data export button
    data_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a:nth-of-type(3) > span:nth-of-type(1)')))
    data_button.click()

    # Save the webpage as a JSON file
    wait.until(lambda d: d.current_url.find("data") == 27)
    if driver.current_url.find("data") == 27:
        current_url = driver.current_url
    else:
        raise Exception("The exported timeline was not loaded. Current page: " + driver.current_url)

    # Fetch URL content
    response = requests.get(current_url)
    json_data = response.json()
    save_path = "/Users/michael/Library/CloudStorage/OneDrive-Personal/Documents/2023/projects/forfun/LibbyBookBackup/libbytimeline-activities.json"

    with open(save_path, "w") as f:
        json.dump(json_data, f, indent=2)

    # Close the browser
    driver.quit()

    return save_path

if __name__ == "__main__":
    export_timeline()