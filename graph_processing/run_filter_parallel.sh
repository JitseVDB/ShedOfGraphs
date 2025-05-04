#!/bin/bash

# Check that we have exactly 2 arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <order> <filter_string>"
  exit 1
fi

ORDER=$1
FILTER_STRING=$2

# Print info about history tracking
echo "Running filter for graphs of order $ORDER with filter:"
echo "$FILTER_STRING"
echo "Filtered graphs will be written to separate files per batch, and history will be saved to history.txt."

# Split the graph generation into multiple batches using the 'res/mod' function or another method
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
    python3 ./filter_graph.py "$FILTER_STRING" < "$batch_file" > "$OUTPUT_DIR/output_batch_$BATCH_NUMBER.txt" &
done

# Wait for all parallel jobs to finish
wait

# After processing, optionally save the history
echo "History saved to history.txt."

# Optionally, process the output files further or combine them as needed
cat $OUTPUT_DIR/output_batch_*.txt > "$OUTPUT_DIR/final_filtered_graphs.txt"
echo "All filtered graphs saved to $OUTPUT_DIR/final_filtered_graphs.txt."
