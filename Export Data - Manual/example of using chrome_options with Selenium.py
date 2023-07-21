from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
user_agent, profile_location = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "/Users/$USER/Library/Application Support/Google/Chrome/LibbyProfile"
chrome_options.arguments.extend([f"user-agent={user_agent}", f"user-data-dir={profile_location}"]) # , "--headless"])
driver = webdriver.Chrome(options=chrome_options)
driver.close()