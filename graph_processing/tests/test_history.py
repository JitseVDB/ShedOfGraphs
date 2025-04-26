from graph_processing.history import HistoryEntry

def test_history_entry_to_line():
    """
    Unit test for the HistoryEntry.to_line() method.

    This test creates a sample HistoryEntry object and verifies that:
        - The tab-delimited output string contains exactly 5 parts.
        - The input_number, output_number, filter_str, and passed_graph_list fields
          match the expected values.
        - The timestamp field is ignored for checking since it is dynamically generated.

    Assertions:
        - The output line must split into exactly 5 tab-separated parts.
        - The second part (index 1) must match the input_number ("10").
        - The third part (index 2) must match the output_number ("5").
        - The fourth part (index 3) must match the filter_str ("degree-sum filter").
        - The fifth part (index 4) must match the passed_graph_list ("graph1,graph3,graph5,graph7,graph9").
    """
    entry = HistoryEntry(
        input_number=10,
        output_number=5,
        filter_str="degree-sum filter",
        passed_graph_list=["graph1", "graph3", "graph5", "graph7", "graph9"]
    )

    line = entry.to_line()
    parts = line.split('\t')

    # Check if line has 5 parts
    assert len(parts) == 5

    # Check values (ignore timestamp for now)
    assert parts[1] == "10"
    assert parts[2] == "5"
    assert parts[3] == "degree-sum filter"
    assert parts[4] == "graph1,graph3,graph5,graph7,graph9"