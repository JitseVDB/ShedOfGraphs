
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
import subprocess
import os
from datetime import datetime
from export_graph6toImage import export_graph_image
import json

"""
Flask web server for the Shed of Graphs project.

This app allows users to:
- Submit graph filtering jobs based on degree-sum rules
- View recently processed graphs from history
- Automatically generate and serve images of filtered graphs

Depends on:
- filter_graph.py for graph filtering
- run_filter_parallel.sh to run filtering in parallel
- export_graph_image() to generate graph images
"""

# Create a Flask application instance
app = Flask(__name__)

# Paths for the history file and the graph images folder
HISTORY_PATH = os.path.expanduser("./history.txt")
GRAPH_IMAGES_FOLDER = os.path.join(os.path.expanduser("~"), "ShedOfGraphs", "graph_processing", "graph_images")

# Ensure the images folder exists
os.makedirs(GRAPH_IMAGES_FOLDER, exist_ok=True)

def load_recent_graphs():
    """
    Reads the history.txt file and extracts the most recent 20 individual passed graphs.
    """
    entries = [] # Initialize entries as an empty list

    # If the history file does not exist yet, return an empty list
    if not os.path.exists(HISTORY_PATH):
        return entries

    # Open and parse each line in the history file
    with open(HISTORY_PATH, "r") as f:
        for line in f:
            # Each line is expected to contain exactly 5 tab-separated fields
            parts = line.strip().split('\t')
            if len(parts) != 5:
                continue # Skip lines that are malformed

            timestamp_str, _, _, filter_used, graph6_list = parts

            # Parse the timestamp; skip the line if it fails
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            
            # Each passed graph is listed in graph6 format, separated by commas
            graphs = graph6_list.split(',')
            for graph in graphs:
                entries.append({
                    "timestamp": timestamp,
                    "graph6": graph,
                    "filter": filter_used
                })

    # Sort all collected graph entries by timestamp (most recent first)
    entries.sort(key=lambda x: x["timestamp"], reverse=True)

    # Return the 20 most recent graph entries
    return entries[:20]

def get_image_url(graph6_str):
    """
    Generates the image for the graph if it doesn't already exist and returns the image URL.
    """
    # Sanitize the graph6 string so it can safely be used as a filename
    safe_graph_name = graph6_str.replace("?", "_q_").replace("/", "_slash_")
    
    # Construct the full path to where the PNG image should be saved
    image_path = os.path.join(GRAPH_IMAGES_FOLDER, f"{safe_graph_name}.png")

     # If the image file doesn't already exist, generate it using the export function
    if not os.path.exists(image_path):
        export_graph_image(graph6_str, "png", GRAPH_IMAGES_FOLDER)
    
    # Return the relative URL used by the Flask route to serve this image
    return f"/static/graph_images/{safe_graph_name}.png"

@app.route("/index")
def index():
    """
    Flask route for /index. Renders the most recent processed graphs and their images.
    """
    # Retrieve a list of the 20 most recently passed graphs from history
    recent_graphs = load_recent_graphs()

    # For each graph, attach an image URL (generating image if necessary)
    for graph in recent_graphs:
        graph["image_url"] = get_image_url(graph["graph6"])
    
    # Render the template with the graph data
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
    """
    Serves a requested graph image file from the local graph_images directory.
    """
    return send_from_directory(GRAPH_IMAGES_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)