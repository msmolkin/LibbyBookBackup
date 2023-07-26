# !/bin/bash

# Description: Download a book from Libby as a single HTML file
# Dependencies: monolith, wget
# Usage: ./download_book_html.sh
# Author: @msmolkin
# License: MIT
mkdir books 2>/dev/null
for url in "https://share.libbyapp.com/data/2cedd9ea-d865-44b8-b4a9-9da9affafa09/libbyjourney-671481-the-100-startup.html"
do
    chrome --headless --dump-dom $url | monolith - -ab https://share.libbyapp.com -j -o book.html
    sed -i '.bak' "s%local source%$url%" book.html
    title=$(python3 extract_notes_title.py) && mv book.html "books/$title.html"
done
rm book.html.bak