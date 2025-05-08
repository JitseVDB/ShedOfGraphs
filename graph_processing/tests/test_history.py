import unittest
import os
from history import HistoryEntry
from history_management import load_history, save_history, HISTORY_FILE

class TestHistory(unittest.TestCase):

    def setUp(self):
        """
        Backup the existing history file if it exists and delete it to start fresh for testing.
        """
        # Backup existing history file if it exists
        self.backup = None
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                self.backup = f.read()
            os.remove(HISTORY_FILE)  # Start fresh for testing

    def tearDown(self):
        """
        Restore the history file from the backup if one exists, otherwise remove the test history file.
        """
        # Restore history file if backup was made
        if self.backup is not None:
            with open(HISTORY_FILE, 'w') as f:
                f.write(self.backup)
        elif os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    def test_history_entry_to_line(self):
        """
        Test the conversion of a HistoryEntry object to a tab-separated line format.
        """
        entry = HistoryEntry(10, 5, '[{"type": "min", "degree_sum": 6, "count": 2}]', ["G1", "G2"])
        line = entry.to_line()
        parts = line.strip().split('\t')
        self.assertEqual(len(parts), 5)
        self.assertEqual(parts[1], "10")
        self.assertEqual(parts[2], "5")
        self.assertEqual(parts[3], '[{"type": "min", "degree_sum": 6, "count": 2}]')
        self.assertEqual(parts[4], "G1,G2")

    def test_save_and_load_history(self):
        """
        Test saving and loading the history, ensuring that data is correctly stored and retrieved.
        """
        entry1 = HistoryEntry(3, 2, "filterA", ["A", "B"])
        entry2 = HistoryEntry(5, 3, "filterB", ["C", "D", "E"])
        save_history([entry1, entry2])

        loaded = load_history()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].input_number, 3)
        self.assertEqual(loaded[1].output_number, 3)
        self.assertEqual(loaded[1].passed_graph_list, ["C", "D", "E"])

    def test_load_history_with_invalid_lines(self):
        """
        Test loading history with invalid lines, ensuring that invalid entries are skipped.
        """
        # Write some invalid entries to the history file
        with open(HISTORY_FILE, 'w') as f:
            f.write("2025-05-05 12:00:00\t3\t2\tfilterA\tG1,G2\n")
            f.write("INVALID LINE WITH TOO FEW FIELDS\n")
            f.write("2025-05-05 12:00:01\t5\t3\tfilterB\tG3,G4,G5\n")

        history = load_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].filter_str, "filterA")
        self.assertEqual(history[1].passed_graph_list, ["G3", "G4", "G5"])

    def test_load_history_empty_file(self):
        """
        Test loading history from an empty file, expecting an empty history list.
        """
        open(HISTORY_FILE, 'w').close()  # Create empty file
        history = load_history()
        self.assertEqual(history, [])

    def test_save_and_load_with_escaped_filter(self):
        """
        Test saving and loading history entries with filters containing special characters.
        """
        # Test filter with special characters
        special_filter = '[{"type": "min", "degree_sum": 6, "count": 2}]'
        entry = HistoryEntry(4, 2, special_filter, ["H1", "H2"])
        save_history([entry])
        history = load_history()
        self.assertEqual(history[0].filter_str, special_filter)
        self.assertEqual(history[0].passed_graph_list, ["H1", "H2"])


if __name__ == '__main__':
    unittest.main()
