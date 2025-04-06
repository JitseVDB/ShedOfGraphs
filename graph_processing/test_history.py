from history import HistoryEntry

def test_history_entry():
    """
    Test the functionality of the HistoryEntry class by creating an instance 
    with sample data and printing its tab-delimited string representation.
    
    This function demonstrates how to create a HistoryEntry object and 
    how the to_line method formats the data for output.
    """
    
    # Sample data for the history entry
    input_number = 10  # Number of input graphs
    output_number = 5  # Number of output graphs
    filter_str = "degree-sum filter"  # Example filter
    passed_graph_list = ["graph1", "graph3", "graph5", "graph7", "graph9"]  # Example passed graphs

    # Create a HistoryEntry instance
    entry = HistoryEntry(input_number, output_number, filter_str, passed_graph_list)

    # Print the tab-delimited string representation of the entry
    # This will display the HistoryEntry in the following format:
    # timestamp\tinput_number\toutput_number\tfilter\tpassed_graph_list
    print(entry.to_line())


# Run the test
if __name__ == "__main__":
    test_history_entry()
