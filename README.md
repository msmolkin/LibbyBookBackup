2. [run python file to automatically download user's libby timeline](<using_code_interpreter/download_timeline.py>) (assumes that you are signed in in the browser)
3. [nodejs puppeteer file to download the book journeys](using_code_interpreter/download_book_json_synchronous.js)
4. [remove any duplicates created when I ran the puppeteer script multiple times](using_code_interpreter/remove_duplicate_files.py)

## 2024-01-23

Before running for the first time (or, if you have to reinstall the headless browser):
1. Set up Libby in this headless browser.
    1. Open the export_timeline.py file and set it to pause at line 20.
    2. Run the file. It will open a browser window. On the main page > "Get Help" > "Reset app" > "Yes, I have a library card" > Follow the instructions to set the code from your phone.
    3. Actions > Synchronize Shelf
    4. Actions > Export Timeline can be done manually or left to the script.
    5. Close the browser window.