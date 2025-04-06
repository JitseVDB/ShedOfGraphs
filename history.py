import time

class HistoryEntry:
    """
    A class to represent a history entry of processed graphs.

    This class stores the timestamp, number of input and output graphs,
    the filter applied during the processing, and the list of graphs that
    passed the filter.

    Attributes:
    ----------
    timestamp : str
        The timestamp of when the entry is created, formatted as 'YYYY-MM-DD HH:MM:SS'.
    input_number : int
        The number of graphs that were input for processing.
    output_number : int
        The number of graphs that passed the filter during processing.
    filter_str : str
        The filter that was applied during the graph processing.
    passed_graph_list : list
        A list of identifiers for the 20 most recent graphs that passed the filter.
    """
    def __init__(self, input_number, output_number, filter_str, passed_graph_list):
        """
        Initializes a HistoryEntry instance with the given parameters.

        Parameters:
        ----------
        input_number : int
            The number of graphs that were input for processing.
        output_number : int
            The number of graphs that passed the filter.
        filter_str : str
            The filter applied during processing.
        passed_graph_list : list
            A list of identifiers for the 20 most recent passed graphs.
        """
        # Timestamp when the entry is created (format: YYYY-MM-DD HH:MM:SS)
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.input_number = input_number  # The number of input graphs
        self.output_number = output_number  # The number of output graphs
        self.filter_str = filter_str  # The filter used during processing
        self.passed_graph_list = passed_graph_list  # List of passed graphs (only the 20 most recent)

    def to_line(self):
        """
        Converts the HistoryEntry instance into a tab-delimited string format.

        This method generates a line formatted as:
        <timestamp>	<inputNumber>	<outputNumber>	<filter>	<passedGraphList>
        
        The list of passed graphs is represented as a comma-separated string.

        Returns:
        -------
        str
            A tab-delimited string representing the history entry.
        """
        # Join the passed graph list into a comma-separated string
        passed_graph_str = ",".join(self.passed_graph_list)
        return f"{self.timestamp}\t{self.input_number}\t{self.output_number}\t{self.filter_str}\t{passed_graph_str}"
