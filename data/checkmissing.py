import os
import json

# Paths to directories
icons_dir = "icons"
apps_dir = "apps"
output_json = "output.json"
log_file = "missing_files.log"

# Read the output.json file
try:
    with open(output_json, "r") as file:
        apps = json.load(file)
except FileNotFoundError:
    print(f"Error: {output_json} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: {output_json} is not a valid JSON file.")
    exit(1)

# Prepare a list to store missing files
missing_files = []

# Loop through each app in the JSON file
for app in apps:
    app_id = app.get("ID")
    if not app_id:
        print(f"Skipping an app with missing ID: {app}")
        continue

    icon_path = os.path.join(icons_dir, f"{app_id}.png")
    compose_path = os.path.join(apps_dir, f"{app_id}.yml")

    missing = []

    # Check for icon
    if not os.path.isfile(icon_path):
        missing.append("icon")

    # Check for compose file
    if not os.path.isfile(compose_path):
        missing.append("compose file")

    # If either is missing, add to the log
    if missing:
        missing_files.append(f"App ID: {app_id} - Missing: {', '.join(missing)}")

# Write the log file
if missing_files:
    with open(log_file, "w") as log:
        log.write("Missing files report:\n")
        log.write("\n".join(missing_files))
    print(f"Missing files logged in {log_file}.")
else:
    print("All files are present.")
