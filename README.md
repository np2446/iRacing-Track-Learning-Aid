# iRacing Track Learning Aid
This is a simple tool to help you learn the tracks in iRacing. It will show you the track map and the corner names. You can also add your own notes to each corner (in development).

This script is designed to interact with the iRacing simulator using the pyirsdk library. It allows users to select a JSON file containing track sector data, preprocesses this data for efficient lookup, and then continuously checks the current sector based on the user's track percentage. If the user is approaching a sector, it will print the approaching sector's name.

## Prerequisites
- Python 3.x
- iRacing SDK (pyirsdk)
- A directory named `track_jsons` containing JSON files with sector data (included in this repository with one example track, Nordschleife-Industriefahrten.json)

## Installation
1. **Install pyirsdk**:
   ```bash
   pip install pyirsdk
    ```

2.	**(Optional) Add your own JSON Files**:
	- Place your JSON files containing sector data in the track_jsons directory.
    - You can also use the included example JSON file, Nordschleife-Industriefahrten.json.

## JSON File Format
Each JSON file should follow this format:

```json
{
    "Sectors": {
        "SectorName1": {"start": 0.0, "end": 0.1},
        "SectorName2": {"start": 0.1, "end": 0.2},
        ...
    }
}
```

## Usage
1. **Run the script**:
   ```bash
   python app.py
   ```

2. **Select a track**:
   - The script will prompt you to select a track from the available JSON files in the `track_jsons` directory.

3. **Drive on iRacing**:
    - The script will continuously check the current sector based on your track percentage in iRacing.
    - If you are approaching a sector, it will print the approaching sector's name.

## Future Improvements (coming ASAP)
- Add the ability to add notes to each corner.
- Improve the user interface for selecting tracks.
- Add more tracks to the `track_jsons` directory.
- Add an overlay UI for iRacing that displays the current sector name.
