import os
import json
from datetime import datetime
import hashlib

def generate_unique_id(path, name):
    """Generate a unique identifier based on path and name"""
    unique_string = f"{path}{name}{datetime.now().isoformat()}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:12]

def create_app_catalog(base_path):
    """Create a catalog of all applications"""
    catalog = {
        'generated_at': datetime.now().isoformat(),
        'apps': []
    }

    # Get the absolute path of the base directory for relative path calculations
    base_abs_path = os.path.abspath(base_path)

    for dir_name in os.listdir(base_path):
        dir_path = os.path.join(base_path, dir_name)
        
        if not os.path.isdir(dir_path):
            continue

        description_path = os.path.join(dir_path, 'description.json')
        
        # Skip if no description.json exists
        if not os.path.exists(description_path):
            continue

        # Calculate relative path from the script location
        relative_path = os.path.relpath(dir_path, start=os.getcwd())

        app_entry = {
            'id': generate_unique_id(relative_path, dir_name),
            'name': dir_name,
            'path': relative_path.replace('\\', '/'),  # Convert Windows paths to forward slashes
            'last_modified': datetime.fromtimestamp(os.path.getmtime(description_path)).isoformat()
        }

        # Get description data with proper encoding handling
        try:
            with open(description_path, 'r', encoding='utf-8') as f:
                description_data = json.load(f)
                # Remove 'tags' field if it exists
                if 'tags' in description_data:
                    del description_data['tags']
                app_entry.update(description_data)
        except UnicodeDecodeError:
            try:
                # Try with a different encoding if UTF-8 fails
                with open(description_path, 'r', encoding='utf-8-sig') as f:
                    description_data = json.load(f)
                    # Remove 'tags' field if it exists
                    if 'tags' in description_data:
                        del description_data['tags']
                    app_entry.update(description_data)
            except Exception as e:
                print(f"Error reading {description_path}: {str(e)}")
                app_entry['description_error'] = f'Error reading file: {str(e)}'
                continue
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {description_path}: {str(e)}")
            app_entry['description_error'] = 'Invalid description.json format'
            continue
        except Exception as e:
            print(f"Unexpected error with {description_path}: {str(e)}")
            app_entry['description_error'] = f'Unexpected error: {str(e)}'
            continue

        catalog['apps'].append(app_entry)

    return catalog

def main():
    servapps_path = "apps"  # Replace with actual path if different
    if not os.path.exists(servapps_path):
        print(f"Error: Directory '{servapps_path}' not found")
        return

    try:
        catalog = create_app_catalog(servapps_path)
        
        # Save the catalog with UTF-8 encoding
        output_path = "apps.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        print(f"Catalog generated successfully at {output_path}")
        print(f"Total apps cataloged: {len(catalog['apps'])}")
    except Exception as e:
        print(f"Error generating catalog: {str(e)}")

if __name__ == "__main__":
    main()