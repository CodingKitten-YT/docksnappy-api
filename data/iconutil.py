import os
import json
import requests
from wand.image import Image
import shutil  # For clearing the terminal

# Define paths to the log and JSON files
LOG_FILE = "missing_files.log"
JSON_FILE = "output.json"
ICONS_DIR = "icons"  # Directory to save downloaded icons

# Create the icons directory if it doesn't exist
os.makedirs(ICONS_DIR, exist_ok=True)

def clear_terminal():
    """Clear the terminal output."""
    shutil.get_terminal_size()  # Ensure cross-platform support
    os.system("cls" if os.name == "nt" else "clear")

def read_missing_files(log_file):
    """Read missing files from the log file."""
    missing_entries = []
    with open(log_file, "r") as file:
        for line in file:
            if "Missing:" in line:
                parts = line.strip().split(" - ")
                app_id = parts[0].replace("App ID: ", "").strip()
                missing = parts[1].replace("Missing: ", "").strip()
                missing_entries.append({"App ID": app_id, "Missing": missing})
    return missing_entries

def load_app_info(json_file):
    """Load app information from the JSON file."""
    with open(json_file, "r") as file:
        return json.load(file)

def find_app_by_id(apps, app_id):
    """Find app information by App ID."""
    for app in apps:
        if app.get("ID") == app_id:
            return app
    return None

def process_icon(icon_source, save_path):
    """Process the icon from a URL or local file path."""
    try:
        if os.path.exists(icon_source):  # Check if it's a local file path
            with Image(filename=icon_source) as img:
                img.format = 'png'
                img.save(filename=save_path)
            print(f"Local file processed and saved at: {save_path}")
        else:  # Assume it's a URL
            response = requests.get(icon_source, stream=True)
            response.raise_for_status()

            # Save content temporarily
            temp_svg_path = "temp_icon.svg"
            with open(temp_svg_path, "wb") as temp_file:
                temp_file.write(response.content)

            # Convert SVG to PNG
            with Image(filename=temp_svg_path) as img:
                img.format = 'png'
                img.save(filename=save_path)

            os.remove(temp_svg_path)  # Cleanup
            print(f"URL icon processed and saved at: {save_path}")

        return True
    except Exception as e:
        print(f"Error processing icon: {e}")
        return False

def main():
    # Load data
    missing_entries = read_missing_files(LOG_FILE)
    apps_data = load_app_info(JSON_FILE)

    for entry in missing_entries:
        app_id = entry["App ID"]
        missing = entry["Missing"]

        if missing == "icon":
            app_info = find_app_by_id(apps_data, app_id)

            if app_info:
                print(f"App Name: {app_info['Name']}")
                print(f"Description: {app_info['Description']}")
                print(f"Source Code: {app_info['Source Code']}")
                print(f"License: {app_info['License']}")
                print(f"Tag: {app_info['Tag']}")

                while True:
                    icon_source = input(
                        f"Enter the icon URL or file path for '{app_info['Name']}' (App ID: {app_id}): "
                    ).strip()
                    if icon_source:
                        save_path = os.path.join(ICONS_DIR, f"{app_id}.png")
                        if process_icon(icon_source, save_path):
                            clear_terminal()  # Clear terminal after successful processing
                            print(
                                f"Icon for '{app_info['Name']}' successfully downloaded and converted."
                            )
                            break
                        else:
                            print("Failed to process the icon. Please try again.")
                    else:
                        print("Icon source cannot be empty. Please try again.")
            else:
                print(f"No app information found for App ID: {app_id}.")

if __name__ == "__main__":
    main()
