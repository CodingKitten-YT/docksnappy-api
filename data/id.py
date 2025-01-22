import json
import random
import string
import os

def generate_unique_id(existing_ids):
    """Generate a unique 5-character ID with 3 digits and 2 lowercase letters in random order, not in the existing_ids set."""
    while True:
        components = random.choices(string.digits, k=3) + random.choices(string.ascii_lowercase, k=2)
        random.shuffle(components)
        unique_id = ''.join(components)
        if unique_id not in existing_ids:
            return unique_id

def add_unique_ids_to_apps(file_path):
    """Add unique 5-character IDs to each app in the JSON file, replacing existing IDs if present."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    try:
        with open(file_path, 'r') as file:
            apps = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading {file_path}: {e}")
        return

    existing_ids = set()
    for app in apps:
        unique_id = generate_unique_id(existing_ids)
        app["ID"] = unique_id
        existing_ids.add(unique_id)

    try:
        with open(file_path, 'w') as file:
            json.dump(apps, file, indent=4)
        print(f"Successfully added or replaced unique IDs in apps in {file_path}.")
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")

if __name__ == "__main__":
    add_unique_ids_to_apps("output.json")
