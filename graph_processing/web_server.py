from flask import Flask, render_template
import os
from datetime import datetime

# Create a Flask application instance
app = Flask(__name__)

# Path to the history.txt file (expanded to user's home directory)
HISTORY_PATH = os.path.expanduser("~/ShedOfGraphs/graph_processing/history.txt")

def load_recent_graphs():
    """
    Reads the history.txt file and extracts the most recent 20 individual passed graphs.
    
    Each line in the file represents a filtering session that may pass multiple graphs.
    This function splits each line into individual graphs, attaches the timestamp and filter
    used to each graph, and returns a list of the 20 most recent graphs sorted by timestamp.
    
    Returns:
        A list of dictionaries, each with keys: "timestamp", "graph6", and "filter".
    """
    entries = []

    # If the file doesn't exist, return an empty list
    if not os.path.exists(HISTORY_PATH):
        return entries

    with open(HISTORY_PATH, "r") as f:
        for line in f:
            # Each line should have 5 tab-separated fields
            parts = line.strip().split('\t')
            if len(parts) != 5:
                continue  # skip malformed lines

            timestamp_str, _, _, filter_used, graph6_list = parts

            try:
                # Parse timestamp into a datetime object
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue  # skip lines with invalid timestamps

            # Extract individual graph6 strings
            graphs = graph6_list.split(',')

            # Create a separate entry for each graph6 string
            for graph in graphs:
                entries.append({
                    "timestamp": timestamp,
                    "graph6": graph,
                    "filter": filter_used
                })

    # Sort entries by timestamp (most recent first), and keep only the last 20
    entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return entries[:20]

@app.route("/index")
def index():
    """
    Flask route for /index.
    Loads the 20 most recent processed graphs and renders them in an HTML table.
    
    Returns:
        Rendered HTML page (index.html) with a table of graph data.
    """
    recent_graphs = load_recent_graphs()
    return render_template("index.html", graphs=recent_graphs)

# Start the Flask development server if this file is run directly
if __name__ == "__main__":
    # Enable debug mode for development
    app.run(debug=True)
