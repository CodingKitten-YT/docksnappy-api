import os
import requests
from bs4 import BeautifulSoup
import json

# Paths
LOG_FILE = "missing_files.log"
APPS_DATA_FILE = "output.json"
OUTPUT_DIR = "icons"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_missing_log(file_path):
    """Parses the missing files log to extract app IDs."""
    missing_ids = []
    with open(file_path, "r") as file:
        for line in file:
            if "App ID:" in line:
                app_id = line.split("App ID:")[1].split("-")[0].strip()
                missing_ids.append(app_id)
    return missing_ids

def load_apps_data(file_path):
    """Loads the apps data from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def get_source_url(app_id, apps_data):
    """Finds the source URL for the given app ID."""
    for app in apps_data:
        if app["ID"] == app_id:
            return app.get("Source Code")
    return None

def get_github_profile_url(repo_url):
    """Extracts the GitHub profile URL from the repository URL."""
    parts = repo_url.split("/")
    if len(parts) >= 4:  # Ensure it's a valid GitHub URL
        user_or_org = parts[3]
        # If repo name matches the user/org name, it's likely a profile URL
        if len(parts) == 5 and parts[4] == user_or_org:
            return repo_url  # Direct profile URL
        return f"{parts[0]}//{parts[2]}/{user_or_org}"
    return None

def download_avatar(profile_url, output_path):
    """Downloads the avatar from the GitHub profile."""
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img", class_="avatar")
        if img_tag and "src" in img_tag.attrs:
            img_url = img_tag["src"]
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                with open(output_path, "wb") as img_file:
                    img_file.write(img_response.content)
                print(f"Downloaded icon for {output_path}")
            else:
                print(f"Failed to download image from {img_url}")
        else:
            print(f"No avatar found on profile page: {profile_url}")
    else:
        print(f"Failed to access profile URL: {profile_url}")

def main():
    # Parse missing files log and load apps data
    missing_ids = parse_missing_log(LOG_FILE)
    apps_data = load_apps_data(APPS_DATA_FILE)

    for app_id in missing_ids:
        print(f"Processing App ID: {app_id}")
        source_url = get_source_url(app_id, apps_data)

        if not source_url:
            print(f"Source URL not found for App ID: {app_id}")
            continue

        profile_url = get_github_profile_url(source_url)
        if not profile_url:
            print(f"Invalid GitHub URL for App ID: {app_id}")
            continue

        output_path = os.path.join(OUTPUT_DIR, f"{app_id}.png")
        download_avatar(profile_url, output_path)

if __name__ == "__main__":
    main()
