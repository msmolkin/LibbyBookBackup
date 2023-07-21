import subprocess
import json
import os
from datetime import datetime

def run_node_script(script_path, book_url):
    result = subprocess.run(['node', script_path, book_url], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running script: {result.stderr}")
        return None
    return json.loads(result.stdout)

def save_json(data, folder="books"):
    timestamp = max(item["timestamp"] for item in data["circulation"])
    date1 = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H-%M")
    current_date = datetime.now().strftime("%Y-%m-%d %H-%M")
    title = data["readingJourney"]["title"]["text"]
    author = data["readingJourney"]["author"]
    
    filename = f"Book {date1} {title} by {author} book notes (downloaded {current_date}).json"
    path = os.path.join(folder, filename)
    
    with open(path, 'w') as file:
        json.dump(data, file)
    
    print(f"Saved to {path}")

script_path = 'download_book_json.js'
journey_url = 'https://libbyapp.com/library/sfpl/similar-3390606/page-1/3390606/journey/3390606' # example

json_file_path = 'Export Data - Manual/libbytimeline-activities.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Here, data is the data from the previous step, from the libbytimeline-activities.json file
for book in data['timeline']:
    journey_url = book["reading_journey_url"]

    book_json_data = run_node_script(script_path, journey_url)
    if book_json_data is not None:
        save_json(book_json_data)
