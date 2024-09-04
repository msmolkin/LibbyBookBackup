import json
import requests
import asyncio
import aiohttp
import os
import logging
from tqdm import tqdm

API_URL = 'https://thunder.api.overdrive.com/v2/media/bulk?titleIds='
HEADERS = {'x-client-id': 'dewey'}
# This is close to the maximum number of titleIds that can be fetched in a single request from this thunder API. Experiment with this number to find the optimal value.
CHUNK_SIZE = 200
OUTPUT_DIR = 'all_overdrive_books'
os.makedirs(OUTPUT_DIR, exist_ok=True)
LOG_FILE = os.path.join(OUTPUT_DIR, 'download_log.txt')

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
            elif response.status == 404:
                logging.error(f"Error {response.status} occurred in fetch_book_data while fetching chunk {chunk_number}. Continuing to next chunk.")
                logging.error(f"URL: {url[:98] + '...' + url[-10:] if len(url) > 110 else url}") # Cleaning it up for my terminal width
                return 0  # TODO: Handle the case where these specific books are no longer available, e.g. with book 1111
            else:
                logging.error(f"Error fetching chunk {chunk_number}: {response.status}")
                return 0
    except Exception as e:
        logging.error(f"Exception occurred while fetching chunk {chunk_number}: {str(e)}")
        return 0

async def download_all_books(title_ids, download_all=False):
    # Total number of books in their library is 11200000
    total_books = 0
    chunk_number = 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        chunk_start = 1
        if download_all:
            # Parallel
            # The issue was just that I was trying to download too many at once. Smaller chunks worked.
            while True:
                chunk = list(range(chunk_start, chunk_start + CHUNK_SIZE))
                chunk_number += 1
                task = asyncio.create_task(fetch_book_data(session, chunk, chunk_number))
                tasks.append(task)
                chunk_start += CHUNK_SIZE
                if len(tasks) >= 10:  # Process 10 chunks at a time
                    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Downloading chunks"):
                        books_in_chunk = await task
                        total_books += books_in_chunk
                        if books_in_chunk == 0:
                            logging.info(f"No books found in chunk. This might indicate we've reached the end of available books.")
                            return total_books
                    tasks = []
            
            # Sequentially download all the books
            # for chunk_start in tqdm(range(1, 11200000//CHUNK_SIZE + 1, CHUNK_SIZE), desc="Downloading chunks"):
            #     chunk = list(range(chunk_start, chunk_start + CHUNK_SIZE))
            #     chunk_number += 1
            #     books_in_chunk = await fetch_book_data(session, chunk, chunk_number)
            #     total_books += books_in_chunk
            #     if books_in_chunk == 0:
            #         logging.info(f"No books found in chunk. This might indicate we've reached the end of available books.")
            #         break
                
        else:
            for i in range(0, len(title_ids), CHUNK_SIZE):
                chunk = title_ids[i:i+CHUNK_SIZE]
                chunk_number += 1
                task = asyncio.create_task(fetch_book_data(session, chunk, chunk_number))
                tasks.append(task)

            for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Downloading chunks"):
                books_in_chunk = await task
                total_books += books_in_chunk
                if books_in_chunk == 0:
                    logging.info(f"No books found in chunk. Reached the limit or encountered an error. Stopping download")
                    break

    logging.info(f"Total books downloaded: {total_books}")
    return total_books

def combine_files(combined_file):
    all_data = {}
    # First, load existing data if the combined file exists
    if os.path.exists(combined_file):
        with open(combined_file, 'r') as file:
            existing_data = json.load(file)
            all_data = {book['id']: book for book in existing_data}
    
    # Then, process all chunk files
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.json') and filename.startswith('chunk_') and filename != os.path.basename(combined_file):
            with open(os.path.join(OUTPUT_DIR, filename), 'r') as file:
                chunk_data = json.load(file)
                for book in chunk_data:
                    all_data[book['id']] = book
    
    # Convert the dictionary back to a list
    final_data = list(all_data.values())
    
    with open(combined_file, 'w') as file:
        json.dump(final_data, file, indent=2)
    logging.info(f"Combined all data into {combined_file}. Total unique books: {len(final_data)}")


def download_books_i_have_read():
    with open('libbytimeline-activities.json', 'r') as file:
        timeline_data = json.load(file)
        
    combined_file = os.path.join(OUTPUT_DIR, 'books_i_have_read.json')

    title_ids = [book["title"]["titleId"] for book in timeline_data['timeline']]
    
    logging.info(f"Starting download of {len(title_ids)} books")
    total_books = asyncio.run(download_all_books(title_ids))
    
    if total_books > 0:
        combine_files(combined_file)

    logging.info("Download process completed successfully")

def download_all_their_books():
    combined_file = os.path.join(OUTPUT_DIR, 'all_overdrive_books.json')
    
    logging.info(f"Starting download of all their books")
    total_books = asyncio.run(download_all_books((), download_all=True))
    
    if total_books > 0:
        combine_files(combined_file)
    
    logging.info("Download process completed successfully")
    
def main():
    try:
        # Delete any existing chunk files
        # [os.remove(os.path.join(OUTPUT_DIR, filename)) for filename in os.listdir(OUTPUT_DIR) if filename.startswith('chunk_')]

        # Eventually, ensure that only one of these functions can be run at a time
        # probably using a lockfile.lock. For now, just run one at a time.
        
        # a) To download just the books I've read
        # download_books_i_have_read()
        
        # b) To download all their books
        download_all_their_books()
        
        # [os.remove(os.path.join(OUTPUT_DIR, filename)) for filename in os.listdir(OUTPUT_DIR) if filename.startswith('chunk_')]  # Delete the chunk files
        # Don't delete the chunk files, because I want to be able to resume if they reject requests.
    
    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Exiting gracefully.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    main()