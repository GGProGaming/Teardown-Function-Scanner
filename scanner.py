import os
import json
from collections import Counter

# Load function names from JSON file
# Adjust the open to be routed to where you have place the file
with open('function_names.json') as f:
    FUNCTIONS = json.load(f) 

# Track points per function
points = Counter()

# Track number of files scanned
num_files = 0

# Recursively walk folder structure
def scan_files(folder):
    global num_files
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.lua'):
                print(f'Scanning {os.path.join(root, file)}...')
                num_files += 1
                path = os.path.join(root, file)
                # Validate path before opening
                if not os.path.exists(path):
                    print(f"{path} does not exist, skipping")
                    continue 
                try:
                    with open(os.path.join(root, file), encoding='utf-8') as f:
                        for line in f:
                            for func in FUNCTIONS:
                                if func in line:
                                    points[func] += 1
                except UnicodeDecodeError:
                    print(f"Unable to decode {file}, skipping")
                    continue
                except OSError as e:
                    print(f"Error opening {path}: {e}")
                    continue



# Main program
if __name__ == '__main__':
    folder = input('Enter folder to scan: ')
    print(f'Scanning folder {folder}')

    scan_files(folder)

    # After scanning is complete                
    print(f'\nScanned {num_files} lua files total') 

    print('\nResults:')
    for func, count in points.most_common():
        print(f'{func}: {count} points')


print('\nDone!')