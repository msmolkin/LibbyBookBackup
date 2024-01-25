import os
import hashlib
import re
from collections import defaultdict
from datetime import datetime

directory = "books"
num_files = len([filename for filename in os.listdir(directory) if filename.startswith("Book") and filename.endswith(".json")])

# Store file contents and their respective paths
file_contents = defaultdict(list)

# Replace the img\d+.od-cdn.com with img_REPLACE.od-cdn.com to make the file contents comparable for duplicates
def normalize_file_content(content):
    return re.sub(r'img\d+\.od-cdn\.com', 'img_REPLACE.od-cdn.com', content)

# Get the hash of each file
def get_sha256_of_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for buf in iter(lambda: f.read(8192), b''):
            hasher.update(buf)
    return hasher.hexdigest()

# Get the hash of file content
def get_sha256_of_text(content):
    hasher = hashlib.sha256()
    hasher.update(content.encode('utf-8'))
    return hasher.hexdigest()

for filename in os.listdir(directory):
    if filename.startswith("Book") and filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        book_title = " ".join(filepath.split(" ")[3:filepath.split(" ").index("by")])

        print(f"Opening book {book_title} ({len(file_contents) + 1} / {num_files})")

        # Open the file and read the contents
        try:
            with open(filepath, 'r') as f:
                file_content = f.read()
            # file_hash = get_file_sha256(filepath)
        except TimeoutError:
            print("If OneDrive is not running. Please start it and try again.")
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error reading file {filepath}: {e}")
            continue
        
        # Exclude the different CDN servers from the file content for comparison
        normalized_content = normalize_file_content(file_content)
        file_hash = get_sha256_of_text(normalized_content)
        
        # Exclude the download date from the filename for comparison
        comparable_filename = " ".join(filename.split(" ")[:-4])

        # Add the file content and filepath to the dictionary
        file_contents[(comparable_filename, file_hash)].append(filepath)

deleted_files_count = 0

# Check for duplicates and remove the newer files
for files in file_contents.values():
    if len(files) > 1:
        # Sort the filepaths by the download date and time in descending order
        files.sort(key=lambda x: datetime.strptime(x.split(" ")[-2] + " " + x.split(" ")[-1].rstrip(").json"), "%Y-%m-%d %H-%M"), reverse=True)
        
        # Remove all but the first (oldest) file
        for f in files[1:]:
            os.remove(f)
            deleted_files_count += 1
            print(f"Deleted file {f} ({deleted_files_count})")

# If this remove_duplicate_files.py deletion file is running, then that means the downloads were all successful, so we can delete the downloaded_books.txt file
if os.path.exists("downloaded_books.txt"): os.remove("downloaded_books.txt")
print(f"Deleted {deleted_files_count} files.")