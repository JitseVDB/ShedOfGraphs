#!/bin/bash

# Check that we have at least 2 arguments
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <order> <filter_string> [--export <folder>] [--image <format>]"
  exit 1
fi

ORDER=$1
FILTER_STRING=$2

# Shift the first two arguments to get optional args
shift 2
OPTIONAL_ARGS=("$@")

# Print info about history tracking and export options
echo "Running filter for graphs of order $ORDER with filter:"
echo "$FILTER_STRING"
echo "Filtered graphs will be printed to stdout, and history will be saved to history.txt."

if [[ "${OPTIONAL_ARGS[*]}" =~ "--export" ]]; then
  echo "Images of filtered graphs will be exported."
fi

# Run geng and pipe output into the Python filter with optional args
geng "$ORDER" | python3 filter_graph.py "$FILTER_STRING" "${OPTIONAL_ARGS[@]}"
