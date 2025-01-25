import os
import json
import requests
import cairosvg
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

def download_icon(url, save_path):
    """Download an icon from the given URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # Check if the file is an SVG
        content_type = response.headers.get("Content-Type", "").lower()
        if "svg" in content_type:
            svg_content = response.content
            # Convert SVG to PNG and save
            cairosvg.svg2png(bytestring=svg_content, write_to=save_path)
            print(f"SVG converted to PNG and saved at: {save_path}")
        else:
            # Save directly as a PNG
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"PNG saved at: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading or converting icon: {e}")
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
                    icon_url = input(f"Enter the icon URL for '{app_info['Name']}' (App ID: {app_id}): ").strip()
                    if icon_url:
                        save_path = os.path.join(ICONS_DIR, f"{app_id}.png")
                        if download_icon(icon_url, save_path):
                            clear_terminal()  # Clear terminal after successful download
                            print(f"Icon for '{app_info['Name']}' successfully downloaded and converted.")
                            break
                        else:
                            print("Failed to download the icon. Please try again.")
                    else:
                        print("Icon URL cannot be empty. Please try again.")
            else:
                print(f"No app information found for App ID: {app_id}.")

if __name__ == "__main__":
    main()
