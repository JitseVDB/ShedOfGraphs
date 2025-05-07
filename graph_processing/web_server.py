from flask import Flask, render_template, send_from_directory
import os
from datetime import datetime
from export_graph6toImage import export_graph_image  # Import the graph image export function

# Create a Flask application instance
app = Flask(__name__)

# Paths for the history file and the graph images folder
HISTORY_PATH = os.path.expanduser("~/ShedOfGraphs/graph_processing/history.txt")
GRAPH_IMAGES_FOLDER = os.path.join(os.path.expanduser("~"), "ShedOfGraphs", "graph_processing", "graph_images")

# Ensure the images folder exists
os.makedirs(GRAPH_IMAGES_FOLDER, exist_ok=True)

def load_recent_graphs():
    """
    Reads the history.txt file and extracts the most recent 20 individual passed graphs.
    
    Returns:
        A list of dictionaries, each with keys: "timestamp", "graph6", and "filter".
    """
    entries = []

    if not os.path.exists(HISTORY_PATH):
        return entries

    with open(HISTORY_PATH, "r") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 5:
                continue

            timestamp_str, _, _, filter_used, graph6_list = parts

            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            graphs = graph6_list.split(',')
            for graph in graphs:
                entries.append({
                    "timestamp": timestamp,
                    "graph6": graph,
                    "filter": filter_used
                })

    entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return entries[:20]

def get_image_url(graph6_str):
    """
    Generates the image for the graph if it doesn't already exist and returns the image URL.
    
    Parameters:
        graph6_str (str): The graph6 string of the graph.
    
    Returns:
        str: The URL to the generated image.
    """
    # Safe filename generation for the image
    safe_graph_name = graph6_str.replace("?", "_q_").replace("/", "_slash_")
    image_path = os.path.join(GRAPH_IMAGES_FOLDER, f"{safe_graph_name}.png")

    if not os.path.exists(image_path):
        # Generate the image if it doesn't exist
        export_graph_image(graph6_str, "png", GRAPH_IMAGES_FOLDER)
    
    return f"/static/graph_images/{safe_graph_name}.png"

@app.route("/index")
def index():
    """
    Flask route for /index. Renders the most recent processed graphs and their images.
    
    Returns:
        Rendered HTML page (index.html) with a table of graph data and images.
    """
    recent_graphs = load_recent_graphs()
    # Add the image URL for each graph
    for graph in recent_graphs:
        graph["image_url"] = get_image_url(graph["graph6"])
    
    return render_template("index.html", graphs=recent_graphs)

# Serve images from the 'graph_images' folder under '/static/graph_images'
@app.route("/static/graph_images/<filename>")
def serve_image(filename):
    return send_from_directory(GRAPH_IMAGES_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
