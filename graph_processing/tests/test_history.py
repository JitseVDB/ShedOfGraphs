from graph_processing.history import HistoryEntry
from graph_processing.history_management import load_history, save_history
import os

def test_history_entry():
    """
    Test that a HistoryEntry object correctly formats itself
    into a tab-separated string with all necessary information.
    """
    entry = HistoryEntry(
        input_number=10,
        output_number=5,
        filter_str="degree-sum filter",
        passed_graph_list=["graph1", "graph3", "graph5"]
    )

    # Test the tab-delimited output of the entry
    line = entry.to_line()
    assert line.startswith("20")  # Should start with the year in the timestamp
    assert "\t10\t5\tdegree-sum filter\tgraph1,graph3,graph5" in line

def test_save_history():
    """
    Test saving a list of HistoryEntry objects to 'history.txt'
    and verify that they are correctly written and can be reloaded.
    """
    entry = HistoryEntry(
        input_number=10,
        output_number=5,
        filter_str="degree-sum filter",
        passed_graph_list=["graph1", "graph3", "graph5"]
    )

    # Save the entry to history.txt
    save_history([entry])

    # Ensure the history file was created
    assert os.path.exists("history.txt")

    # Load the saved history and check content
    history = load_history()
    assert len(history) == 1
    assert history[0].input_number == 10
    assert history[0].output_number == 5

def test_load_history_empty_file():
    """
    Test that loading history from an empty 'history.txt' file
    correctly returns an empty list without errors.
    """
    # Ensure the history file is empty
    if os.path.exists("history.txt"):
        os.remove("history.txt")
    
    history = load_history()
    assert len(history) == 0  # No entries should be loaded

def test_incomplete_history_data():
    """
    Test that loading malformed/incomplete history data
    (missing passed graphs list) results in no loaded entries.
    """
    # Create a malformed history entry
    with open("history.txt", "w") as f:
        f.write("2025-04-26 12:00:00\t10\t5\tdegree-sum filter\n")  # Missing passed_graph_list field

    history = load_history()
    assert len(history) == 0  # Malformed entry should be skipped or cause load to fail gracefully
