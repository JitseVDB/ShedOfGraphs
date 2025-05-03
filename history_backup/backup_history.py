#!/usr/bin/env python3
"""
backup_history.py

This script creates a timestamped backup of the history file used in ShedOfGraphs.

- Source file: ~/ShedOfGraphs/history.txt
- Backup destination: ~/ShedOfGraphs/.filtered-graphs/
- Backup filename format: history_YYYYMMDD_HHMM.txt

The script ensures the backup directory exists and does not overwrite previous backups.
"""

import os
import shutil
from datetime import datetime

def main():
    """
    Main function to perform the backup operation.
    """
    # Define source and destination paths
    source_file = os.path.expanduser('~/ShedOfGraphs/history.txt')
    backup_dir = os.path.expanduser('~/ShedOfGraphs/.filtered-graphs/')

    # Ensure that the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Generate a unique backup filename based on the current date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    backup_filename = f'history_{timestamp}.txt'
    backup_path = os.path.join(backup_dir, backup_filename)

    # Attempt to copy the source file to the backup location
    try:
        shutil.copyfile(source_file, backup_path)
        print(f"Backup created successfully: {backup_path}")
    except FileNotFoundError:
        print("Error: Source history file not found.")
    except Exception as e:
        print(f"Unexpected error during backup: {e}")

if __name__ == "__main__":
    main()