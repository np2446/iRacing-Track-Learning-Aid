import os
import json
import irsdk

class State:
    ir_connected = False

def get_json_files(directory: str) -> list:
    """
    Returns a list of JSON files in the specified directory.

    Args:
        directory (str): The directory path to search for JSON files.

    Returns:
        list: A list of JSON file names.

    """
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def load_json_file(directory: str, filename: str) -> dict:
    """
    Load a JSON file from the specified directory.

    Args:
        directory (str): The directory where the JSON file is located.
        filename (str): The name of the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file is not a valid JSON file.

    """
    with open(os.path.join(directory, filename), 'r') as file:
        return json.load(file)
    
def check_iracing():
    """
    Checks the status of the iRacing connection and performs necessary actions.

    If the iRacing connection is currently established but the iRacing SDK is not initialized
    or not connected, the function will disconnect and print a message.

    If the iRacing connection is not established but the iRacing SDK is initialized and connected,
    the function will establish the connection and print a message.

    """
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def preprocess_sectors(sectors: dict) -> list:
    """
    Preprocesses the sectors dictionary and creates a lookup table for sector names based on their range.
    This allows the lookup of the sector to be O(1) instead of O(n) at the cost of memory (negligible, tens of KB).

    Args:
        sectors (dict): A dictionary containing sector names as keys and their corresponding range as values.

    Returns:
        list: A lookup table where each index represents a position on the track and the value at that index is the sector name.

    """
    track_length = 1.0
    lookup = [None] * int(track_length * 10000)
    
    for sector_name, sector_range in sectors.items():
        start_index = int(sector_range['start'] * 10000)
        end_index = int(sector_range['end'] * 10000)
        for i in range(start_index, end_index + 1):
            lookup[i] = sector_name
    
    return lookup

def find_sector(track_pct: float, lookup: list) -> str:
    """
    Finds the sector based on the given track percentage.

    Parameters:
    track_pct (float): The track percentage.
    lookup (list): The lookup list containing sectors.

    Returns:
    str: The sector corresponding to the track percentage.
    """

    index = int(track_pct * 10000)
    sector = lookup[index]
    
    if sector:
        return sector
    
    for i in range(index, len(lookup)):
        if lookup[i]:
            return f"approaching {lookup[i]}"
    
    return "Sector not found"

def main():
    """
    Main function that performs the following steps:
    1. Checks if the specified directory exists.
    2. Retrieves a list of JSON files in the directory.
    3. Displays the available JSON files to the user.
    4. Prompts the user to select a JSON file.
    5. Loads the selected JSON file and extracts sector data.
    6. Preprocesses the sector data for efficient lookup.
    7. Connects to the iRacing simulator.
    8. Continuously checks the current sector based on the simulator data.
    9. Handles keyboard interrupt to gracefully exit the program.
    10. Shuts down the iRacing connection.

    Raises:
        RuntimeError: If the specified directory does not exist or if no JSON files are found in the directory.
        ValueError: If an invalid choice is made when selecting a JSON file.
    """
    directory = 'track_jsons'
    
    if not os.path.exists(directory):
        raise RuntimeError(f"The directory '{directory}' does not exist")
    
    json_files = get_json_files(directory)
    
    if not json_files:
        raise RuntimeError(f"No JSON files found in the directory '{directory}'")
    
    print("Available JSON files:")
    for idx, file in enumerate(json_files, start=1):
        print(f"{idx}. {file}")
    
    choice = int(input("Select the JSON file to use (number): ")) - 1
    
    if choice < 0 or choice >= len(json_files):
        raise ValueError("Invalid choice")
    
    json_file = json_files[choice]
    sectors_data = load_json_file(directory, json_file)
    
    sectors = sectors_data.get('Sectors', {})
    
    if not sectors:
        raise RuntimeError("No sectors data found in the JSON file")
    
    lookup = preprocess_sectors(sectors)

    ir = irsdk.IRSDK()
    state = State()

    try:
        while True:
            check_iracing()
            if state.ir_connected:
                track_pct = ir["LapDistPct"]
            sector = find_sector(track_pct, lookup)
            print(f"Current sector: {sector}")

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if state.ir_connected:
            ir.shutdown()

if __name__ == "__main__":
    main()
