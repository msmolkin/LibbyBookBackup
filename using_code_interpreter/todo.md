Remaining:
Replace the `download_book_json_synchronous.js` file with an asynchronous version. This will allow for the book journey jsons to be downloaded simultaneously. This will be (much?) faster than the current synchronous version.

Automate running the python/node files:
`download_timeline.py`, `download_book_json_synchronous.js`, and `remove_duplicate_files.py` should be run in that order. I'll probably do it with a bash script. Maybe os.subprocess.

---

Need to deal with the errors that sometimes pop up: it accidentally opens the book share page (click actions -> button 3) instead of the book journey json (click actions -> button 2 -> button 3).

Afterwards, this happens:
/usr/local/bin/node ./using_code_interpreter/download_book_json_synchronous.js
An error occurred:  Error: Node is either not clickable or not an HTMLElement
    at CDPElementHandle.clickablePoint (/Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/common/ElementHandle.js:176:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async CDPElementHandle.hover (/Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/common/ElementHandle.js:242:26)
    at async IsolatedWorld.hover (/Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/common/IsolatedWorld.js:161:9)
    at async /Users/michael/Library/CloudStorage/OneDrive-Personal/Documents/2023/projects/forfun/LibbyBookBackup/using_code_interpreter/download_book_json_synchronous.js:94:17 {stack: 'Error: Node is either not clickable or not an…reter/download_book_json_synchronous.js:94:17', message: 'Node is either not clickable or not an HTMLElement'}
An error occurred:  Error: Node is either not clickable or not an HTMLElement
    at CDPElementHandle.clickablePoint (/Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/common/ElementHandle.js:176:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async CDPElementHandle.hover (/Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/common/ElementHandle.js:242:26)
    at async IsolatedWorld.hover (/Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/common/IsolatedWorld.js:161:9)
    at async /Users/michael/Library/CloudStorage/OneDrive-Personal/Documents/2023/projects/forfun/LibbyBookBackup/using_code_interpreter/download_book_json_synchronous.js:94:17 {stack: 'Error: Node is either not clickable or not an…reter/download_book_json_synchronous.js:94:17', message: 'Node is either not clickable or not an HTMLElement'}
Uncaught TimeoutError TimeoutError: Navigation timeout of 30000 ms exceeded
    at <anonymous> (file:///Users/michael/node_modules/puppeteer-core/lib/cjs/puppeteer/util/Deferred.js:27:33)
    at listOnTimeout (node:internal/timers:573:17)
    at processTimers (node:internal/timers:514:7)
Process exited with code 1

---

2024-01-23

Before running for the first time (or, if you have to reinstall the headless browser):
1. Set up Libby in this headless browser.
    1. Open the export_timeline.py file and set it to pause at line 20.
    2. Run the file. It will open a browser window. On the main page > "Get Help" > "Reset app" > "Yes, I have a library card" > Follow the instructions to set the code from your phone.
    3. Actions > Synchronize Shelf
    4. Actions > Export Timeline can be done manually or left to the script.

`using_code_interpreter/export_timeline.py:export_timeline():save_path` is hardcoded to my path. Should be changed to a relative path.

---

2024-01-24

Copilot: I'm going to try to make the puppeteer script asynchronous. I'm not sure how to do this, but I'll try to figure it out.

Also: I should make a failsafe. When I get the TimeoutError from above, I should delete the books up to and including the last one that successfully finished from the timeline (libbytimeline-activities.json file)). Then, I should have it run the script again. (This will allow me to run the script overnight without worrying about it failing.)
Alternatively, I can make a list of the books that finished, and then run the script again but have it check if the book is in the list of books that finished. If it is, then it will skip it. This might be faster than deleting the books from the timeline.
Thought: this is a common problem in programming interviews. If you have a list of success and a list of fail, how do you only run on the failures? Copilot: I think the answer is to use a hash table. I'll try to implement this.