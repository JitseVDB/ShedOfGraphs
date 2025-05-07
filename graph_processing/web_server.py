from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
import subprocess
import os
from datetime import datetime
from export_graph6toImage import export_graph_image
import json

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
    """
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
    """
    recent_graphs = load_recent_graphs()
    for graph in recent_graphs:
        graph["image_url"] = get_image_url(graph["graph6"])
    
    return render_template("index.html", graphs=recent_graphs)

@app.route("/filter_graphs", methods=["POST"])
def filter_graphs():
    """
    Handles the form submission to filter graphs based on user input and generate the filter string.
    """
    # Extract the form fields
    try:
        vertices = int(request.form["vertices"])
        degree_sum = int(request.form["degree_sum"])
        filter_type = request.form["filter_type"]
        count = int(request.form["count"])

        # Validate that no value is negative
        if vertices < 0 or degree_sum < 0 or count < 0:
            raise ValueError("Input values must be non-negative")

    except (ValueError, TypeError):
        # Handle invalid inputs (negative values or wrong data types)
        return "Invalid input, all values must be non-negative integers", 400

    # Build the filter rules JSON
    filter_rule = [{
        "degree_sum": degree_sum,
        "type": filter_type,
        "count": count
    }]
    
    filter_string = json.dumps(filter_rule)

    # Define the shell command to run the filtering script
    command = [
        "./run_filter_parallel.sh",  # Path to the shell script
        str(vertices),               # Pass the number of vertices
        filter_string,               # Pass the filter string
        "--export",                  # Option to export images
        "./graph_images",            # Directory for image export
        "--image",                   # Image format option
        "png"                        # Image format
    ]
    
    try:
        # Run the command using subprocess
        subprocess.run(command, check=True)
        print("Filter executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the filter: {e}")
        return "Error executing the filter", 500

    # After processing, redirect to the index page to view the results
    return redirect(url_for('index'))

# Serve images from the 'graph_images' folder under '/static/graph_images'
@app.route("/static/graph_images/<filename>")
def serve_image(filename):
    return send_from_directory(GRAPH_IMAGES_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
