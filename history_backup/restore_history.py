#!/usr/bin/env python3
"""
restore_history.py

This script restores the history file from one of the available backups in ShedOfGraphs.

- Backup directory: ~/.filtered-graphs/
- Source file: ~/ShedOfGraphs/history.txt
- Backup filename format: history_YYYYMMDD_HHMM.txt

The script lists all available backups in the backup directory, allows the user to select a backup, 
and then restores the selected backup over the current history file.
If no backups are found, an error message will be displayed.
"""

import os
import shutil

# Paths
backup_dir = os.path.expanduser('~/.filtered-graphs/')
source_file = os.path.expanduser('~/ShedOfGraphs/history.txt')

# List all backup files (history_*.txt)
try:
    backups = [f for f in os.listdir(backup_dir) if f.startswith('history_') and f.endswith('.txt')]
    
    if not backups:
        print("No backup files found in the backup directory.")
        exit()

    print("Available backups:")
    # Show available backups with a numbered list
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")

    # Let user choose a backup to restore
    choice = int(input("Enter the number of the backup to restore: "))
    
    # Validate input
    if choice < 1 or choice > len(backups):
        print("Invalid choice.")
        exit()

    # Get the selected backup file
    selected_backup = backups[choice - 1]
    selected_backup_path = os.path.join(backup_dir, selected_backup)

    # Perform the restore (copy selected backup to the source file location)
    shutil.copyfile(selected_backup_path, source_file)
    print(f"Restored {selected_backup} to {source_file}")

except Exception as e:
    print(f"Error: {e}")
