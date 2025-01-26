import json

# Define URLs using placeholders for ID
icon_url_template = "https://cdn.jsdelivr.net/gh/CodingKitten-YT/docksnappy-api/data/icons/{}.png"
compose_url_template = "https://cdn.jsdelivr.net/gh/CodingKitten-YT/docksnappy-api/data/apps/{}.yml"

# Load the data from output.json
with open('output.json', 'r') as file:
    data = json.load(file)

# Add icon_url and docker_compose_url to each item
for item in data:
    app_id = item.get('ID')  # Use 'ID' from the JSON structure
    
    if app_id:
        # Construct URLs
        item['icon_url'] = icon_url_template.format(app_id)
        item['docker_compose_url'] = compose_url_template.format(app_id)

# Save the updated data back into output.json
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)

print("URLs added successfully.")
