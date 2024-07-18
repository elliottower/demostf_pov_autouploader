import os
import argparse
import requests
from datetime import datetime, timezone, timedelta
from tzlocal import get_localzone

from demostf_pov_autouploader import PROJECT_ROOT

DEMO_API_BASE_URL = "https://api.demos.tf"

def calculate_ticks(time_diff):
    # 66.67 ticks per second
    return int(time_diff.total_seconds() * 66.67)

def get_real_start_ticks(demo_time: datetime, stv_demo_time: datetime, stv_demo_duration_seconds: int):
    time_diff = stv_demo_time - demo_time
    total_ticks = int(time_diff.total_seconds() * 66.67)
    stv_ticks = int(stv_demo_duration_seconds * 66.67)
    return total_ticks - stv_ticks


def extract_filename(demo_file):
    filename = os.path.basename(demo_file)
    return filename

def convert_unix_to_datetime(unix_timestamp, local_timezone):
    utc_dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    local_dt = utc_dt.astimezone(local_timezone)
    return local_dt



def extract_datetime_from_filename(filename, local_timezone):
    base_name, ext = os.path.splitext(filename)
    if ext == '.dem':
        try:
            # Parse the datetime as a naive local time
            naive_local_dt = datetime.strptime(base_name, '%Y-%m-%d_%H-%M-%S')
            # Replace the naive datetime's timezone with the local timezone
            local_dt = naive_local_dt.replace(tzinfo=local_timezone)
            return local_dt
        except ValueError as e:
            print(f"Error parsing datetime from filename: {e}")
            return None
    return None

def fetch_demos(steam_id, start_date, end_date):
    url = f"{DEMO_API_BASE_URL}/profiles/{steam_id}"
    params = {
        'after': int(start_date.timestamp()),
        'before': int(end_date.timestamp()),
        'order': 'ASC'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch demos: {response.status_code} {response.text}")
        return []

def extract_metadata(demo_file_path, steam_id):
    # Detect the local timezone
    local_timezone = get_localzone()

    # print("Steam ID: ", steam_id)
    # print("Demo filepath: ", demo_file_path)
    demo_filename = extract_filename(demo_file_path)
    demo_time = extract_datetime_from_filename(demo_filename, local_timezone)

    if not demo_time:
        print("Failed to extract timestamp from filename.")
        return

    # Calculate the start and end of the day in UTC
    start_date = demo_time.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
    end_date = start_date + timedelta(days=1)

    print("Original POV demo: ", demo_filename)
    print("Time:", demo_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    demos = fetch_demos(steam_id, start_date, end_date)

    if not demos:
        print("No demos found for the given date.")
        return

    closest_demo = None
    min_time_diff = None

    for demo in demos:
        demo_details = requests.get(f"{DEMO_API_BASE_URL}/demos/{demo['id']}").json()
        demo_end_time = datetime.fromtimestamp(demo_details['time'], tz=timezone.utc)

        if demo_end_time > demo_time:
            time_diff = demo_end_time - demo_time
            if min_time_diff is None or time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_demo = demo_details

    if closest_demo:
        # Manually extract demos.tf link, player alias, and make title for new upload
        demos_tf_link = f"https://demos.tf/{closest_demo['id']}"
        player = next((player for player in closest_demo['players'] if player['steamid'] == str(steam_id)), None)
        pov_demo_title = f"{closest_demo['server']} - {closest_demo['red']} vs {closest_demo['blue']} - {player['name']}"

        # Calculate real start tick for POV demo
        stv_demo_time = convert_unix_to_datetime(closest_demo['time'], local_timezone)
        stv_demo_duration = closest_demo['duration']
        real_start_ticks = get_real_start_ticks(demo_time, stv_demo_time, stv_demo_duration)

        print(f"\nClosest STV found: {closest_demo['name']} ({demos_tf_link})")
        print(f"Map: {closest_demo['map']}")
        print(f"Time: {stv_demo_time}")
        print(f"Duration: {stv_demo_duration} seconds")
        print(f"Real start ticks for POV demo: {real_start_ticks}")
        print(f"Server: {closest_demo['server']}")
        print(f"Nickname: {closest_demo['nick']}")
        print(f"ID: {closest_demo['id']}")
        print(f"Download Link: {closest_demo['url']}")
        print(f"Red Team: {closest_demo['red']} - Score: {closest_demo['redScore']}")
        print(f"Blue Team: {closest_demo['blue']} - Score: {closest_demo['blueScore']}")
        print("Players:")
        for player in closest_demo['players']:
            print(
                f"  - {player['name']} ({player['class']}) - Kills: {player['kills']}, Assists: {player['assists']}, Deaths: {player['deaths']}")
        return pov_demo_title, closest_demo['red'], closest_demo['blue']
    else:
        print("No matching demo found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and display metadata for a TF2 demo file.')
    EXAMPLE_DEMO_PATH = os.path.join(PROJECT_ROOT, "2024-06-11_22-39-08.dem")
    EXAMPLE_STEAM_ID = 76561198059645150
    parser.add_argument('--demo_file', type=str, help='Absolute path to the demo file', default=EXAMPLE_DEMO_PATH)
    parser.add_argument('--steam_id', type=str, help='Steam ID (steamid64) of the player', default=EXAMPLE_STEAM_ID)
    args = parser.parse_args()

    extract_metadata(demo_file_path=args.demo_file, steam_id=args.steam_id)
