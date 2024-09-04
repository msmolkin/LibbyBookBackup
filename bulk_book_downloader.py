import json
import requests
import asyncio
import aiohttp
import os
import logging
from tqdm import tqdm

API_URL = 'https://thunder.api.overdrive.com/v2/media/bulk?titleIds='
HEADERS = {'x-client-id': 'dewey'}
CHUNK_SIZE = 10000
OUTPUT_DIR = 'all_overdrive_books'
os.makedirs(OUTPUT_DIR, exist_ok=True)
LOG_FILE = os.path.join(OUTPUT_DIR, 'download_log.txt')
COMBINED_FILE = os.path.join(OUTPUT_DIR, 'all_overdrive_books.json')

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_book_data(session, title_ids, chunk_number):
    url = f"{API_URL}{','.join(map(str, title_ids))}"
    try:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                filename = f"{OUTPUT_DIR}/chunk_{chunk_number}.json"
                with open(filename, 'w') as file:
                    json.dump(data, file, indent=2)
                logging.info(f"Downloaded chunk {chunk_number}")
                return len(data)
            elif response.status == 429:
                logging.warning(f"Rate limit hit for chunk {chunk_number}. Retrying after 60 seconds.")
                await asyncio.sleep(60)
                return await fetch_book_data(session, title_ids, chunk_number)
            else:
                logging.error(f"Error fetching chunk {chunk_number}: {response.status}")
                return 0
    except Exception as e:
        logging.error(f"Exception occurred while fetching chunk {chunk_number}: {str(e)}")
        return 0

async def download_all_books(title_ids):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_books = 0
    chunk_number = 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(0, len(title_ids), CHUNK_SIZE):
            chunk = title_ids[i:i+CHUNK_SIZE]
            chunk_number += 1
            task = asyncio.create_task(fetch_book_data(session, chunk, chunk_number))
            tasks.append(task)

        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Downloading chunks"):
            books_in_chunk = await task
            total_books += books_in_chunk
            if books_in_chunk == 0:
                logging.info(f"Reached the limit or encountered an error. Stopping download.")
                break

    logging.info(f"Total books downloaded: {total_books}")
    return total_books

def combine_files():
    all_data = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(OUTPUT_DIR, filename), 'r') as file:
                all_data.extend(json.load(file))
    
    with open(COMBINED_FILE, 'w') as file:
        json.dump(all_data, file, indent=2)
    logging.info(f"Combined all data into {COMBINED_FILE}")

def main():
    try:
        # Load title IDs from your existing JSON file
        with open('libbytimeline-activities.json', 'r') as file:
            timeline_data = json.load(file)
        
        title_ids = [book["title"]["titleId"] for book in timeline_data['timeline']]
        
        logging.info(f"Starting download of {len(title_ids)} books")
        total_books = asyncio.run(download_all_books(title_ids))
        
        if total_books > 0:
            combine_files()
        
        logging.info("Download process completed successfully")
    
    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Exiting gracefully.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    main()