<!-- 1. headless/all_books_activities.json -->
manually download file (this can be automated, too): https://libbyapp.com/timeline/activities -> click "Actions" -> click "Export timeline" -> click "Data"

2. [run python file](<using_code_interpreter/attempt 1 modified.py>)
3. [nodejs puppeteer file to download the book journeys](using_code_interpreter/download_book_json_synchronous.js)
4. [remove any duplicates created when I ran the puppeteer script multiple times](using_code_interpreter/remove_duplicate_files.py)