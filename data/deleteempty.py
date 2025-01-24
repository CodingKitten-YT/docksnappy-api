import os

# Path to the directory containing compose files
apps_dir = "apps"

# Get a list of all files in the apps directory
try:
    compose_files = [
        os.path.join(apps_dir, file) for file in os.listdir(apps_dir) if file.endswith(".yml")
    ]
except FileNotFoundError:
    print(f"Error: Directory '{apps_dir}' not found.")
    exit(1)

# Initialize a counter for deleted files
deleted_count = 0

# Loop through each compose file
for compose_file in compose_files:
    try:
        # Check if the file is empty
        if os.path.getsize(compose_file) == 0:
            os.remove(compose_file)
            print(f"Deleted empty compose file: {compose_file}")
            deleted_count += 1
    except FileNotFoundError:
        print(f"Warning: File '{compose_file}' was not found.")
    except Exception as e:
        print(f"Error processing file '{compose_file}': {e}")

print(f"Total empty compose files deleted: {deleted_count}")
