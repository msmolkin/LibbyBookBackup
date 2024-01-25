import json
import requests
from export_timeline import export_timeline

JSON_FILE_PATH = 'libbytimeline-activities.json'
COMPLETE_BOOKS_INFO_FILE = 'complete_books_information.json'
API_URL = 'https://thunder.api.overdrive.com/v2/media/bulk?titleIds='
HEADERS = {'x-client-id': 'dewey'}

# Create reading journey URLs and add to JSON data
def add_reading_journey_urls(data):
    for book in data['timeline']:
        id = book["title"]["titleId"]
        book["reading_journey_url"] = f"{book['library']['url']}/similar-{id}/page-1/{id}/journey/{id}"

# Fetch all available data about the books from the OverDrive API
def fetch_book_data(title_ids):
    url = f"{API_URL}{','.join(map(str, title_ids))}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        with open(COMPLETE_BOOKS_INFO_FILE, 'w') as file:
            json.dump(response.json(), file, indent=2)
    else:
        print(f"Error fetching book data: {response.status_code}")

def save_json(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == '__main__':
    # Prepare: get the libby timeline data and save it to a JSON file
    export_timeline()

    with open(JSON_FILE_PATH, 'r') as file:
        timeline_data = json.load(file)

    # title_ids = [book["title"]["titleId"] for book in data['timeline'] if book["activity"] == "Returned"]  # a lot of books never got "returned"
    title_ids = [book["title"]["titleId"] for book in timeline_data['timeline']]
    add_reading_journey_urls(timeline_data)
    save_json(timeline_data, JSON_FILE_PATH)
    fetch_book_data(title_ids)
