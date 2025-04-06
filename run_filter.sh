#!/bin/bash

# Check that we have exactly 2 arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <order> <filter_string>"
  exit 1
fi

ORDER=$1
FILTER_STRING=$2

# Run geng and pipe output into the Python filter
geng $ORDER | python3 filter_graph.py "$FILTER_STRING"
