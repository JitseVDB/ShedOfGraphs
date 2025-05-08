import os
from history import HistoryEntry

HISTORY_FILE = "history.txt"

def load_history():
    """
    Load the processing history from the history file if it exists.

    This function attempts to read the `history.txt` file, parsing each line into a
    `HistoryEntry` object. Each line in the file should represent a history entry with
    the following components: timestamp, input_number, output_number, filter_str, and 
    passed_graph_list (a comma-separated list of graph identifiers). If the file does not 
    exist, an empty list is returned.

    Returns:
        list: A list of `HistoryEntry` objects representing the history of processed graphs.
              An empty list is returned if the history file does not exist or is empty.
    """
    history = []  # Initialize an empty list to store history entries
    
    # Check if the history file exists
    if os.path.exists(HISTORY_FILE):
        # Open the file in read mode
        with open(HISTORY_FILE, 'r') as file:
            # Read each line from the history file
            for line in file:
                # Split the line into components based on tab characters
                parts = line.strip().split('\t')
                
                # Ensure that the line contains exactly 5 components (timestamp, input_number, output_number, filter_str, passed_graph_list)
                if len(parts) == 5:
                    # Extract the components
                    timestamp, input_number, output_number, filter_str, passed_graph_str = parts
                    
                    # Split the passed graphs string by commas to convert it into a list
                    passed_graph_list = passed_graph_str.split(",")
                    
                    # Create a new HistoryEntry object and append it to the history list
                    history.append(HistoryEntry(int(input_number), int(output_number), filter_str, passed_graph_list))
    
    # Return the list of history entries
    return history

def save_history(history):
    """
    Save the processing history to the history file.

    This function appends each history entry from the provided list to the `history.txt`
    file. Each entry is written as a tab-delimited string. If the file does not exist,
    it will be created. The function does not overwrite the file but appends to it.

    Args:
        history (list): A list of `HistoryEntry` objects to be saved. Each entry will be written
                        as a tab-delimited line in the `history.txt` file.
    """
    # Open the history file in append mode
    with open(HISTORY_FILE, 'a') as file:
        # Write each history entry to the file
        for entry in history:
            # Convert the history entry to a tab-delimited line and write it to the file
            file.write(entry.to_line() + '\n')
