#!/bin/bash

# ===============================================================
# Script to generate graphs using 'geng', filter them in parallel
# using a Python script, and optionally export them as images.
#
# Usage:
#   ./run_filter_parallel.sh <order> <filter_string> [--export <folder_path>] [--image <format>]
#
# Required:
#   <order>           : Number of vertices in the graphs to generate (passed to 'geng')
#   <filter_string>   : Filter rules (as a JSON string) for the Python filter
#
# Optional:
#   --export <folder> : Folder where images of filtered graphs will be saved
#   --image <format>  : Image format for exported graphs (e.g., png, svg)
#
# Output:
#   - Filtered graph results will be written to batch files in 'graph_batches'
#   - History is appended to 'history.txt'
#   - Final combined output is saved in 'graph_batches/final_filtered_graphs.txt'
#   - If export is enabled, images of passed graphs are saved to the specified folder
# ===============================================================

# Check that we have exactly 2 arguments (order and filter_string)
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <order> <filter_string> [--export <folder_path>] [--image <format>]"
  exit 1
fi

ORDER=$1
FILTER_STRING=$2
EXPORT_FOLDER=""
IMAGE_FORMAT=""

# Check if the third argument is --export, then grab the folder path
if [ "$3" == "--export" ]; then
  EXPORT_FOLDER=$4
  shift 2  # Shift to the next argument
fi

# Check if the next argument is --image, then grab the image format
if [ "$3" == "--image" ]; then
  IMAGE_FORMAT=$4
  shift 2  # Shift to the next argument
fi

# Print info about history tracking
echo "Running filter for graphs of order $ORDER with filter:"
echo "$FILTER_STRING"
echo "Filtered graphs will be written to separate files per batch, and history will be saved to history.txt."

# Split the graph generation into multiple batches
NUM_BATCHES=4  # Adjust based on how many threads you want to run in parallel
BATCH_SIZE=$(( $(geng $ORDER | wc -l) / NUM_BATCHES ))  # Calculate the size of each batch

# Create a directory for storing batch files and output within the project directory
PROJECT_DIR=$(pwd)  # Get the current project directory
OUTPUT_DIR="$PROJECT_DIR/graph_batches"  # Path to the output directory inside the project folder
mkdir -p "$OUTPUT_DIR"  # Create the directory if it doesn't exist

# Generate batches of graphs and save them to the output directory
geng $ORDER | split -l $BATCH_SIZE - "$OUTPUT_DIR/graph_batch_"

# Run the filtering process in parallel
for batch_file in $OUTPUT_DIR/graph_batch_*; do
    # Use `basename` to extract the batch number for the output file
    BATCH_NUMBER=$(basename $batch_file | sed 's/graph_batch_//')
    
    # Run each filter in parallel, outputting to separate files in the project directory
    if [ -n "$EXPORT_FOLDER" ]; then
        python3 ./filter_graph.py "$FILTER_STRING" --export "$EXPORT_FOLDER" --image "$IMAGE_FORMAT" < "$batch_file" > "$OUTPUT_DIR/output_batch_$BATCH_NUMBER.txt" &
    else
        python3 ./filter_graph.py "$FILTER_STRING" < "$batch_file" > "$OUTPUT_DIR/output_batch_$BATCH_NUMBER.txt" &
    fi
done

# Wait for all parallel jobs to finish
wait

# After processing, optionally save the history
echo "History saved to history.txt."

# Optionally, process the output files further or combine them as needed
cat $OUTPUT_DIR/output_batch_*.txt > "$OUTPUT_DIR/final_filtered_graphs.txt"
echo "All filtered graphs saved to $OUTPUT_DIR/final_filtered_graphs.txt."
