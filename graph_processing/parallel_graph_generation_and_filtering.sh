#!/bin/bash

# ------------------------------------------------------------
# Script to generate and filter graph batches in parallel
# ------------------------------------------------------------
#
# This script:
# 1. Uses Plantri to generate graphs in parallel in multiple batches.
# 2. Filters each generated batch using the `filter_graph.py` script based on a user-defined filter.
# 3. Merges the filtered results into a single file for further use.
#
# Parameters:
# - N_RES: Number of batches (parallel jobs)
# - GRAPH_ORDER: The number of vertices for the generated graphs.
# - PLANTRI_OPTIONS: Plantri options (used for generating specific graph families).
# - FILTER_STRING: A JSON string defining the filtering rules to apply to the graphs.

# PARAMETERS
N_RES=4               # Number of batches
GRAPH_ORDER=10        # Number of vertices in each generated graph
PLANTRI_OPTIONS="-c5" # Plantri options to control the generation process
FILTER_STRING='[{"degree_sum": 6, "type": "min", "count": 3}]' # JSON filter (example)

# Create working directories for raw and filtered graphs (if they don't exist)
mkdir -p raw_batches filtered_batches

# ------------------------------------------------------------
# Step 1: Generate graphs in parallel using Plantri
# ------------------------------------------------------------
# In this step, Plantri is run in parallel for each batch, generating graphs with the specified number of vertices.
# The output graphs are saved in the `raw_batches/` folder.

echo "Starting Plantri batches..."

for RES in $(seq 0 $((N_RES-1))); do
    echo "  Running Plantri res=$RES mod=$N_RES"
    # Generate a batch of graphs using Plantri, redirect the output to raw_batches/graphs_${RES}.g6
    plantri $PLANTRI_OPTIONS $GRAPH_ORDER res=$RES mod=$N_RES > raw_batches/graphs_${RES}.g6 &
done

# Wait for all Plantri processes to finish
wait
echo "All Plantri batches finished."

# ------------------------------------------------------------
# Step 2: Filter each batch in parallel using filter_graph.py
# ------------------------------------------------------------
# Now, we filter the raw graphs using `filter_graph.py`. Each batch is processed in parallel,
# and the filtered graphs are saved in the `filtered_batches/` folder.

echo "Starting filtering batches..."

for RES in $(seq 0 $((N_RES-1))); do
    echo "  Filtering batch $RES"
    # Set PYTHONPATH so Python can find the 'graph_processing' module
    PYTHONPATH=. python3 ./graph_processing/filter_graph.py "$FILTER_STRING" < raw_batches/graphs_${RES}.g6 > filtered_batches/filtered_${RES}.g6 &
done

wait
echo "All filtering batches finished."

# ------------------------------------------------------------
# Step 3: Merge the filtered output into a single file
# ------------------------------------------------------------
# After filtering, we concatenate all the filtered batches into a single file named `final_filtered_graphs.g6`.

echo "Merging filtered batches..."

cat filtered_batches/filtered_*.g6 > final_filtered_graphs.g6

echo "Done! Final filtered graphs are in final_filtered_graphs.g6"
