"""
This is a proof of concept script, to test out uploading a single hard-coded POV demo file.
It currently fails due to issues with the demos.tf upload API (as far as I can tell)
"""
import os
import argparse
import requests
import configparser

from demostf_pov_autouploader import PROJECT_ROOT
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
            print(f"\nAttempting to upload demo: {pov_demo_name}")
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


EXAMPLE_DEMO_PATH = os.path.join(PROJECT_ROOT, "2024-06-11_22-39-08.dem")

def main():
    parser = argparse.ArgumentParser(description='Upload TF2 demos to demos.tf.')
    parser.add_argument('--file', type=str, help='Path to the demo file to upload', default=EXAMPLE_DEMO_PATH)
    args = parser.parse_args()

    demo_file_path = args.file
    demo_folder = os.path.dirname(demo_file_path)
    api_key, steam_id = get_config(demo_folder)

    if not os.path.exists(demo_file_path):
        print(f"Demo file {demo_file_path} does not exist.")
        return

    upload_demo(demo_file_path, api_key, steam_id)


if __name__ == "__main__":
    main()
