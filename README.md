# Shed of Graphs

## Overview
`Shed of Graphs` is a Python tool that filters graphs based on specific edge conditions involving the sum of the degrees of the incident nodes. The filter supports conditions like:
- Minimum a given number of edges where the sum of the degrees is a specific value.
- Maximum a given number of edges where the sum of the degrees is a specific value.
- Exactly a given number of edges where the sum of the degrees is a specific value.

The program reads graphs in the graph6 format, processes them, and outputs only those that satisfy the given conditions.

## Features
- **Graph filtering** based on degree-sum edge conditions.
- Supports rules with `min`, `max`, and `exactly` edge count conditions.
- Can be easily extended to support more complex filtering logic.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/shed-of-graphs.git
    cd shed-of-graphs
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the filter, provide a filter string and pipe graph6 data into the program:

```bash
geng 6 | python filter_graph.py '[{"degree_sum": 6, "type": "min", "count": 3}]'
