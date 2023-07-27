import os
import json
from collections import defaultdict
from datetime import datetime

directory = "books"

# Store file contents and their respective paths
file_contents = defaultdict(list)

for filename in os.listdir(directory):
    if filename.startswith("Book") and filename.endswith(".json"):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
            file_content = json.load(file)
        
        # Exclude the download date from the filename for comparison
        comparable_filename = " ".join(filename.split(" ")[:-4])

        # Add the file content and filepath to the dictionary
        file_contents[(comparable_filename, str(file_content))].append(filepath)

# Check for duplicates and remove the newer files
for files in file_contents.values():
    if len(files) > 1:
        # Sort the filepaths by the download date and time in descending order
        files.sort(key=lambda x: datetime.strptime(x.split(" ")[-2], "%Y-%m-%d %H-%M"), reverse=True)
        
        # Remove all but the first (oldest) file
        for file in files[1:]:
            os.remove(file)
            print(f"Deleted file {file}")
