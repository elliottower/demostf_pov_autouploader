"""This script watches the specified folder and automatically tries to upload demos when it detects them"""
import os
import argparse
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import configparser
import psutil

from demostf_pov_autouploader.fetch_metadata import extract_metadata


def get_config(demo_folder):
    config_file = os.path.join(demo_folder, "demostf_autoupload_config.ini")
    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        api_key = input("Please enter your demos.tf API key: ")
        steam_id = input("Please enter your Steam ID: ")
        config['DEFAULT'] = {'API_KEY': api_key, 'STEAM_ID': steam_id}
        with open(config_file, 'w') as file:
            config.write(file)
    else:
        config.read(config_file)
        api_key = config['DEFAULT'].get('API_KEY')
        steam_id = config['DEFAULT'].get('STEAM_ID')

        if not api_key:
            api_key = input("Please enter your demos.tf API key: ")
            config['DEFAULT']['API_KEY'] = api_key

        if not steam_id:
            steam_id = input("Please enter your Steam ID: ")
            config['DEFAULT']['STEAM_ID'] = steam_id

        with open(config_file, 'w') as file:
            config.write(file)

    return api_key, steam_id


def upload_demo(file_path, api_key, steam_id):
    try:
        with open(file_path, 'rb') as demo_file:
            pov_demo_name, red_team_name, blu_team_name = extract_metadata(demo_file_path=file_path, steam_id=steam_id)
            print(f"Uploading demo: {pov_demo_name}")
            data = {
                'key': api_key,
                'name': pov_demo_name,
                'red': red_team_name,
                'blu': blu_team_name
            }
            files = {
                'demo': demo_file
            }
            response = requests.post('https://api.demos.tf/upload/', data=data, files=files)
            if response.status_code == 200:
                print(f"Successfully uploaded {file_path}")
            else:
                print(f"Failed to upload {file_path}. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while uploading the demo: {e}")


def is_file_closed(file_path):
    for proc in psutil.process_iter(['open_files']):
        if proc.info['open_files']:
            for open_file in proc.info['open_files']:
                if open_file.path == file_path:
                    return False
    return True


class DemoHandler(FileSystemEventHandler):
    def __init__(self, api_key, steam_id):
        self.api_key = api_key
        self.steam_id = steam_id

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.dem'):
            print(f"New demo file detected: {event.src_path}")
            while not is_file_closed(event.src_path):
                time.sleep(1)  # Wait for the file to be closed
            upload_demo(event.src_path, self.api_key, self.steam_id)


def main():
    parser = argparse.ArgumentParser(description='Upload TF2 demos to demos.tf.')
    parser.add_argument('--folder', type=str, required=False, help='Folder to watch for new demo files', default="/Users/elliottower/Documents/GitHub/demostf_pov_autouploader")
    # parser.add_argument('--folder', type=str, help='Folder to watch for new demo files. Default: C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Team Fortress 2\\tf\\demos\\', default="C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Team Fortress 2\\tf\\demos\\")
    args = parser.parse_args()

    demo_folder = args.folder
    api_key, steam_id = get_config(demo_folder)

    observer = Observer()
    event_handler = DemoHandler(api_key, steam_id)
    observer.schedule(event_handler, path=demo_folder, recursive=False)

    observer.start()
    print(f"Watching for new demo files in {demo_folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
