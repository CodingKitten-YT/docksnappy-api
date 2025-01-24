import os
import re

def clean_yaml_files(folder_path):
    """
    Cleans each .yml file in the specified folder by removing all text except for the YAML content.
    If no ```yaml block is present, the file remains unchanged.
    """
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Process only .yml files
        if filename.endswith(".yml"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Extract YAML content between ```yaml and ```
            yaml_content = re.search(r"```yaml(.*?)```", content, re.DOTALL)

            if yaml_content:
                # Save only the content inside ```yaml and ```
                cleaned_content = yaml_content.group(1).strip()

                # Write the cleaned content back to the file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(cleaned_content)

                print(f"Cleaned: {filename}")
            else:
                # If no ```yaml block, skip the file
                print(f"No YAML block found in: {filename}. File left unchanged.")

if __name__ == "__main__":
    # Specify the folder containing .yml files
    apps_folder = "apps"
    clean_yaml_files(apps_folder)
