# !/bin/bash

# Description: Download a book from Libby as a single HTML file
# Dependencies: monolith, wget
# Usage: ./download_book_html.sh
# Author: @msmolkin
# License: MIT
chrome --headless --dump-dom https://share.libbyapp.com/data/128268d1-52c2-4b9a-8f85-302cb791c71d/libbyjourney-6032452-the-body-keeps-the-score.html | monolith - -ab https://share.libbyapp.com -j -o book.html
title=$(python3 extract_notes_title.py) && mv book.html "$title.html"
