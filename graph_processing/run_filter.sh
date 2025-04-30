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
echo "Filtered graphs will be printed to stdout, and history will be saved to history.txt."

# Run geng and pipe output into the Python filter
geng $ORDER | python3 ./graph_processing/filter_graph.py "$FILTER_STRING"
