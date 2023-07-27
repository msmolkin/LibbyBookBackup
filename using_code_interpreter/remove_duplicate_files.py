import os
import json
from collections import defaultdict
from datetime import datetime

directory = "books"
num_files = len([filename for filename in os.listdir(directory) if filename.startswith("Book") and filename.endswith(".json")])

# Store file contents and their respective paths
file_contents = defaultdict(list)

for filename in os.listdir(directory):
    if filename.startswith("Book") and filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        book_title = " ".join(filepath.split(" ")[3:filepath.split(" ").index("by")])

        print(f"Reading book {book_title} ({len(file_contents) + 1} / {num_files})")

        try:
            with open(filepath, 'r') as f:
                file_content = json.load(f)
        except TimeoutError:
            print("If OneDrive is not running. Please start it and try again.")
        
        # Exclude the download date from the filename for comparison
        comparable_filename = " ".join(filename.split(" ")[:-4])

        # Add the file content and filepath to the dictionary
        file_contents[(comparable_filename, str(file_content))].append(filepath)

deleted_files_count = 0
# Check for duplicates and remove the newer files
for files in file_contents.values():
    if len(files) > 1:
        # Sort the filepaths by the download date and time in descending order
        files.sort(key=lambda x: datetime.strptime(x.split(" ")[-2] + " " + x.split(" ")[-1].rstrip(").json"), "%Y-%m-%d %H-%M"), reverse=True)
        
        
        # Remove all but the first (oldest) file
        # keep a count of the number of files deleted. print it each time
        for f in files[1:]:
            os.remove(f)
            deleted_files_count += 1
            print(f"Deleted file {f} ({deleted_files_count})")

print(f"Deleted {deleted_files_count} files.")