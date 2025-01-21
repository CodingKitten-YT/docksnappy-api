import os
import json
import yaml
import re

def process_directory(base_path):
    # Iterate through all subdirectories in the base path
    for dir_name in os.listdir(base_path):
        dir_path = os.path.join(base_path, dir_name)
        
        if not os.path.isdir(dir_path):
            continue
            
        # Delete config.json and icon.png if they exist
        config_path = os.path.join(dir_path, 'config.json')
        icon_path = os.path.join(dir_path, 'icon.png')
        
        if os.path.exists(config_path):
            os.remove(config_path)
            print(f"Deleted {config_path}")
            
        if os.path.exists(icon_path):
            os.remove(icon_path)
            print(f"Deleted {icon_path}")
            
        # Process docker-compose.yml
        docker_compose_path = os.path.join(dir_path, 'docker-compose.yml')
        if os.path.exists(docker_compose_path):
            process_docker_compose(docker_compose_path, dir_name)

def replace_service_name(value, container_name):
    if isinstance(value, str):
        return value.replace('{ServiceName}', container_name)
    elif isinstance(value, dict):
        return {k: replace_service_name(v, container_name) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_service_name(item, container_name) for item in value]
    return value

def process_docker_compose(file_path, dir_name):
    # Read the docker-compose file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Load YAML content
    data = yaml.safe_load(content)
    
    # Remove cosmos-installer if it exists
    if 'cosmos-installer' in data:
        del data['cosmos-installer']
    
    # Process the name field - remove 'big-bear-' prefix if it exists
    if 'name' in data:
        data['name'] = data['name'].replace('big-bear-', '')
    
    # Process services
    if 'services' in data:
        # Get the first (and presumably only) service key
        old_service_key = list(data['services'].keys())[0]
        service_data = data['services'][old_service_key]
        
        # Determine the container name
        container_name = None
        # First check if there's a container_name specified
        if 'container_name' in service_data:
            container_name = service_data['container_name'].replace('{ServiceName}', dir_name)
        # If not, use the directory name as fallback
        if not container_name or container_name == '{ServiceName}':
            container_name = dir_name
        
        # Replace all occurrences of {ServiceName} with the container_name
        new_service_data = replace_service_name(service_data, container_name)
        
        # Update the services section with the directory name as the service key
        data['services'] = {dir_name: new_service_data}
    
    # Write the modified content back to the file
    with open(file_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    
    print(f"Processed {file_path}")

if __name__ == "__main__":
    servapps_path = "apps"  # Replace with actual path if different
    if os.path.exists(servapps_path):
        process_directory(servapps_path)
        print("Processing completed successfully")
    else:
        print(f"Error: Directory '{servapps_path}' not found")