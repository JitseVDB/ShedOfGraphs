#!/bin/bash

# ===============================================================
# Script to generate graphs using 'geng', filter using a Python script, 
# and optionally export them as images.
#
# Usage:
#   ./run_filter.sh <order> <filter_string> [--export <folder>] [--image <format>]
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
#   - Filtered graphs are printed to stdout
#   - History is appended to 'history.txt'
#   - If export is enabled, images of passed graphs are saved to the specified folder
# ===============================================================

# Ensure the script is called with at least two arguments
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <order> <filter_string> [--export <folder>] [--image <format>]"
  exit 1
fi

ORDER=$1          # The order of the graphs to be generated (e.g., 6, 7, 8)
FILTER_STRING=$2  # The filter string (in JSON format) to be applied to the graphs

# Shift the first two arguments, leaving optional arguments in $OPTIONAL_ARGS
shift 2
OPTIONAL_ARGS=("$@")

# Display information about the current run, including filter and optional arguments
echo "Running filter for graphs of order $ORDER with filter:"
echo "$FILTER_STRING"
echo "Filtered graphs will be printed to stdout, and history will be saved to history.txt."

if [[ "${OPTIONAL_ARGS[*]}" =~ "--export" ]]; then
  echo "Images of filtered graphs will be exported."
fi

# Generate graphs using 'geng', then filter them using the Python script 'filter_graph.py'
# Pass the filter string and any optional arguments (e.g., --export, --image) to the Python script
geng "$ORDER" | python3 filter_graph.py "$FILTER_STRING" "${OPTIONAL_ARGS[@]}"
