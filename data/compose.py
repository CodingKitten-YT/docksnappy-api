import os
import json
import logging
import threading
import queue
import subprocess

logging.basicConfig(filename='docker_compose_scraper.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s', 
                    encoding='utf-8')

def generate_docker_compose_with_wizardlm2(app_details):
    try:
        prompt = f"Generate a docker-compose.yml file for {app_details['Name']}. Provide only the docker-compose.yml content in plain text."
        
        for _ in range(3):
            try:
                result = subprocess.run(
                    ['ollama', 'run', 'koesn/wizardlm2-7b', prompt], 
                    capture_output=True, 
                    text=True, 
                    timeout=60,
                    encoding='utf-8',
                    errors='ignore'
                )
                
                compose_content = result.stdout.strip()
                
                if 'version:' in compose_content and 'services:' in compose_content:
                    return compose_content
            except subprocess.TimeoutExpired:
                logging.warning(f"Timeout generating compose for {app_details['Name']}")
            except UnicodeDecodeError:
                logging.warning(f"Unicode decode error for {app_details['Name']}")
        
        return None
    except Exception as e:
        logging.error(f"Wizardlm2 generation error for {app_details['Name']}: {e}")
        return None

def process_single_app(app, result_queue, apps_dir):
    compose_file_path = os.path.join(apps_dir, f"{app['ID']}.yml")
    
    # Check if file exists and is not empty
    if os.path.exists(compose_file_path) and os.path.getsize(compose_file_path) > 0:
        logging.info(f"Skipping {app['Name']} - File already exists and is not empty")
        result_queue.put(None)
        return

    try:
        logging.info(f"Processing {app['Name']} (ID: {app['ID']})")

        docker_compose_content = generate_docker_compose_with_wizardlm2(app)

        if docker_compose_content and not os.path.exists(compose_file_path):
            with open(compose_file_path, 'w', encoding='utf-8') as f:
                f.write(docker_compose_content)
            logging.info(f"Saved Docker Compose for {app['Name']}")
            result_queue.put(None)
        else:
            logging.warning(f"Failed to generate Docker Compose for {app['Name']}")
            result_queue.put(f"{app['Name']} - {app['ID']} - No Docker Compose content")

    except Exception as e:
        logging.error(f"Error processing {app['Name']}: {e}")
        result_queue.put(f"{app['Name']} - {app['ID']} - Unexpected error")

def process_applications(input_json_path='output.json'):
    apps_dir = 'apps'
    os.makedirs(apps_dir, exist_ok=True)
    failed_apps = []

    with open(input_json_path, 'r', encoding='utf-8') as f:
        applications = json.load(f)

    for app in applications:
        result_queue = queue.Queue()
        thread = threading.Thread(target=process_single_app, args=(app, result_queue, apps_dir))
        thread.start()
        thread.join(timeout=60)

        try:
            result = result_queue.get(block=False)
            if result:
                failed_apps.append(result)
        except queue.Empty:
            failed_apps.append(f"{app['Name']} - {app['ID']} - Processing timed out")

    if failed_apps:
        with open('failed_apps.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(failed_apps))
        logging.warning(f"Total failed apps: {len(failed_apps)}")

def main():
    process_applications()

if __name__ == '__main__':
    main()