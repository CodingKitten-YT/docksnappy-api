import json
import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
from tqdm import tqdm

def get_main_color(image_url):
    """Fetch the image from the URL and get its main color in hex."""
    try:
        print(f"Fetching image from: {image_url}")
        response = requests.get(image_url, timeout=10, stream=True)
        response.raise_for_status()

        # Load the image in chunks to bypass size issues
        img = Image.open(BytesIO(response.content))
        
        # Use ColorThief to get the dominant color
        with BytesIO() as buffer:
            img.save(buffer, format="PNG")
            buffer.seek(0)
            color_thief = ColorThief(buffer)
            dominant_color = color_thief.get_color(quality=1)
        
        # Convert RGB to hex
        hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color)
        print(f"Dominant color for {image_url}: {hex_color}")
        return hex_color
    except OSError as e:
        print(f"File size or format issue for {image_url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing image from {image_url}: {e}")
        return None

def process_json(input_file, output_file):
    """Remove 'Tag', calculate main color, and update JSON with verbosity and progress bar."""
    try:
        # Load the JSON data
        with open(input_file, "r") as file:
            data = json.load(file)
        
        print(f"Loaded {len(data)} items from {input_file}.")
        
        # Initialize the progress bar
        for item in tqdm(data, desc="Processing items"):
            print(f"Processing item: {item.get('Name', 'Unknown')}")

            # Remove 'Tag' key if it exists
            if "Tag" in item:
                print(f"Removing 'Tag' from {item.get('Name', 'Unknown')}")
                item.pop("Tag", None)
            
            # Get the main color from the icon URL
            icon_url = item.get("icon_url")
            if icon_url:
                main_color = get_main_color(icon_url)
                if main_color:
                    item["main_color"] = main_color
                else:
                    print(f"Failed to extract color for {item.get('Name', 'Unknown')}")
            else:
                print(f"No icon URL found for {item.get('Name', 'Unknown')}")
        
        # Save the updated data back to the file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Processed JSON saved to {output_file}")
    except Exception as e:
        print(f"Error processing JSON: {e}")

# Specify the input and output file paths
input_file = "output.json"
output_file = "output_updated.json"

# Run the processing function
process_json(input_file, output_file)
