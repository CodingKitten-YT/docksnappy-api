import os
import json
import requests

# Path to the input JSON file and output folder
INPUT_FILE = "output.json"
OUTPUT_FOLDER = "icons"

# Ensure the icons folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the JSON data
with open(INPUT_FILE, "r") as file:
    apps = json.load(file)

# Base URL for icons
BASE_URL = "https://cdn.jsdelivr.net/gh/selfhst/icons/png/"

for app in apps:
    try:
        # Prepare the icon URL and output path
        app_name = app["Name"].lower()
        app_id = app["ID"]
        icon_url = f"{BASE_URL}{app_name}.png"
        output_path = os.path.join(OUTPUT_FOLDER, f"{app_id}.png")
        
        # Fetch the icon
        response = requests.get(icon_url, stream=True)
        
        if response.status_code == 200:
            # Save the icon to the icons folder
            with open(output_path, "wb") as icon_file:
                for chunk in response.iter_content(1024):
                    icon_file.write(chunk)
            print(f"Saved icon for {app['Name']} to {output_path}")
        else:
            print(f"Icon not found for {app['Name']} at {icon_url}")
    except Exception as e:
        print(f"Failed to fetch icon for {app['Name']}: {e}")
