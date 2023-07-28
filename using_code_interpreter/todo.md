Remaining:
Make sure the node.js file works
Rename `attempt 1 modified` files to `download_timeline.py`
Create a readme.md file that says to run the files in order:
    1. `download_timeline.py` and
    2. `download_book_json.py`
    3. `remove_duplicate_files.py`


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
