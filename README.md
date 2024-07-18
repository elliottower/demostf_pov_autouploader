# TF2 POV Demo Auto Uploader

This script automatically uploads TF2 POV demos to demos.tf.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/demostf_pov_autouploader.git
    cd demostf_pov_autouploader
    ```

2. Install the package using pip:
    ```sh
    pip install -e .
    ```

## Usage

### Configuration

The script will prompt you for your demos.tf API key and Steam ID upon first run and save them in the `demostf_autoupload_config.ini` file in the folder where the demo file is located for future use.

### Fetch Metadata

Given a POV demo, to find the corresponding STV demo and fetch associated metadata: 

```bash
python demostf_pov_autouploader/fetch_metadata.py --demo_file 2024-06-11_22-39-08.dem --steam_id 76561198059645150
```

Example Output:
```
Original POV demo:  2024-06-11_22-39-08.dem
Time: 2024-06-11 22:39:08 EDT-0400

Closest STV found: match-20240612-0249-cp_gullywash_f9.dem (https://demos.tf/1149274)
Time: 2024-06-11 23:24:00 EDT-0400
Map: cp_gullywash_f9
Duration: 2050 seconds
Server: na.serveme.tf #559357
Nickname: SourceTV Demo
ID: 1149274
Download Link: https://freezer.demos.tf/a5/2f/a52fa62f10fafa4bfaa7b0542c21bfdb_match-20240612-0249-cp_gullywash_f9.dem
Red Team: RED - Score: 1
Blue Team: BLU - Score: 3
Players:
  - bobo zZᶻ (demoman) - Kills: 19, Assists: 5, Deaths: 11
  - where are yew, i miss yeww。zZ (scout) - Kills: 14, Assists: 13, Deaths: 20
  - Michaelpc1 zZᶻ (scout) - Kills: 35, Assists: 16, Deaths: 12
  - Jarrett (scout) - Kills: 19, Assists: 10, Deaths: 21
  - gnomer (medic) - Kills: 5, Assists: 9, Deaths: 12
  - 1-800-SMK-WEED (soldier) - Kills: 21, Assists: 6, Deaths: 16
  - dearly departed (soldier) - Kills: 23, Assists: 5, Deaths: 21
  - Cronjington Magoo (soldier) - Kills: 16, Assists: 8, Deaths: 28
  - 2 hop harry zZᶻ (medic) - Kills: 0, Assists: 24, Deaths: 9
  - reverie (soldier) - Kills: 20, Assists: 6, Deaths: 28
  - goblin vibewizard (scout) - Kills: 23, Assists: 15, Deaths: 13
  - beware the wide rat (demoman) - Kills: 10, Assists: 11, Deaths: 14

```

* Note that the POV demo timestamp is 22:39:08, whereas the STV is 23:24:00.
  * This means the player joined the server at 10:39 EST, and the STV demo finished recording at 11:24 EST
  * Subtracting these two numbers, we can see that the 

## Upload Demo
To test demo uploading using an example demo:

```bash 
python demostf_pov_autouploader/upload_demo_hardcoded.py --file /path/to/demo_file.dem
```

Example Output:
``` 
Original POV demo:  2024-06-11_22-39-08.dem
Time: 2024-06-11 22:39:08 EDT-0400

Closest STV found: match-20240612-0249-cp_gullywash_f9.dem (https://demos.tf/1149274)
Time: 2024-06-11 23:24:00 EDT-0400
Map: cp_gullywash_f9
Duration: 2050 seconds
Server: na.serveme.tf #559357
Nickname: SourceTV Demo
ID: 1149274
Download Link: https://freezer.demos.tf/a5/2f/a52fa62f10fafa4bfaa7b0542c21bfdb_match-20240612-0249-cp_gullywash_f9.dem
Red Team: RED - Score: 1
Blue Team: BLU - Score: 3
Players:
  - bobo zZᶻ (demoman) - Kills: 19, Assists: 5, Deaths: 11
  - where are yew, i miss yeww。zZ (scout) - Kills: 14, Assists: 13, Deaths: 20
  - Michaelpc1 zZᶻ (scout) - Kills: 35, Assists: 16, Deaths: 12
  - Jarrett (scout) - Kills: 19, Assists: 10, Deaths: 21
  - gnomer (medic) - Kills: 5, Assists: 9, Deaths: 12
  - 1-800-SMK-WEED (soldier) - Kills: 21, Assists: 6, Deaths: 16
  - dearly departed (soldier) - Kills: 23, Assists: 5, Deaths: 21
  - Cronjington Magoo (soldier) - Kills: 16, Assists: 8, Deaths: 28
  - 2 hop harry zZᶻ (medic) - Kills: 0, Assists: 24, Deaths: 9
  - reverie (soldier) - Kills: 20, Assists: 6, Deaths: 28
  - goblin vibewizard (scout) - Kills: 23, Assists: 15, Deaths: 13
  - beware the wide rat (demoman) - Kills: 10, Assists: 11, Deaths: 14

Attempting to upload demo: na.serveme.tf #559357 - RED vs BLU - Cronjington Magoo
Failed to upload /Users/elliottower/Documents/GitHub/demostf_pov_autouploader/2024-06-11_22-39-08.dem. Status code: 404, Response: <h1>404 Not Found</h1><h3>The page you have requested could not be found.</h3>

```

* Note: this currently results in an error, due to issues with the demos.tf upload API.