import requests
import json
import os
import re
from bs4 import BeautifulSoup

# Path to your JSON file
# note: this was downloaded from the Libby website: Navigate to https://libbyapp.com/timeline/activities, Click "Actions" -> "Export Timeline" -> "Data"
json_file_path = 'libbytimeline-activities.json'
# Headers for requests
headers = {'x-client-id': 'dewey'}

with open(json_file_path, 'r') as file:
    data = json.load(file)

title_ids = [book["title"]["titleId"] for book in data]

# Create reading journey URLs and add to JSON data
for book in data:
    id = book["title"]["titleId"]
    book["reading_journey_url"] = book["library"]["url"] + "similar-" + str(id) + "/page-1/" + str(id) + "/journey/" + str(id)

# Save modified JSON file
with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)

# API endpoint
api_url = 'https://thunder.api.overdrive.com/v2/media/bulk?titleIds=' + ','.join(map(str, title_ids)) + '&x-client-id=dewey'

# Send request to API
response = requests.get(api_url, headers=headers)

# Save response to JSON file
if response.status_code == 200:
    with open('complete_books_information.json', 'w') as file:
        json.dump(response.json(), file, indent=4)

# Process each book
for book in data:
    journey_url = book["reading_journey_url"]

    # Get page content
    page = requests.get(journey_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract book_user_connection_id from page
    match = re.search(r'"https://share\.libbyapp\.com/data/(.*)/libbyjourney-', str(soup))
    if match:
        book_user_connection_id = match.group(1)

        # Generate lower_case_title
        title = book["title"]["title"]
        lower_case_title = re.sub(r'[^a-zA-Z0-9 ]', '', title).lower().replace(' ', '-')

        # Construct download URL
        download_url = "https://share.libbyapp.com/data/" + book_user_connection_id + "/libbyjourney-" + str(id) + "-" + lower_case_title + ".json"

        # Download and save file
        response = requests.get(download_url)
        if response.status_code == 200:
            with open('libbyjourney-' + str(id) + '-' + lower_case_title + '.json', 'w') as file:
                json.dump(response.json(), file, indent=4)
