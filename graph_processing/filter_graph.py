import sys
import json
import networkx as nx
import argparse

from history import HistoryEntry
from export_graph6toImage import export_graph_image
from history_management import save_history


"""
filter_graph.py

This script filters graphs based on user-defined rules involving the sum of degrees
of nodes at each edge. It reads graphs in graph6 format from standard input, checks
each graph against a list of rules provided as a JSON string, and prints only the
graphs that satisfy all the rules.

Each rule specifies:
    - "degree_sum": the target sum of degrees of two connected nodes
    - "type": one of "min", "max", or "exactly"
    - "count": how many such edges are required

Usage:
    python filter_graph.py '<filter_string>'

Example:
    python filter_graph.py '[{"degree_sum": 6, "type": "min", "count": 3}]'
    This keeps only graphs with at least 3 edges where the endpoints have degrees summing to 6.

Version: 1.0
"""

def parse_rules(rule_str):
    """
    Parses the filter string into a Python object (dictionary or list) based on the JSON format.

    Args:
        rule_str (str): A JSON-formatted string representing filtering rules.

    Returns:
        list or dict: A Python object representing the parsed rules. 
                    The object will be a dictionary if the JSON string represents an object 
                    or a list if the JSON string represents an array.

    Raises:
        SystemExit: If the `rule_str` is not valid JSON, the function prints an error message 
                    and exits the program with a status code of 1.

    Example:
        >>> parse_rules('{"degree_sum": 6, "type": "min", "count": 2}')
        {'degree_sum': 6, 'type': 'min', 'count': 2}
        >>> parse_rules('[{"degree_sum": 6, "type": "min", "count": 2}]')
        [{'degree_sum': 6, 'type': 'min', 'count': 2}]
    """
    try:
        rules = json.loads(rule_str) 
        return rules
    except json.JSONDecodeError:
        print("Invalid filter string: not valid JSON")
        sys.exit(1)


def matches_rule(edge, degrees, rule):
    """
    Checks if a given edge in the graph satisfies a specific filtering rule based on the degree sum.

    Args:
        edge (tuple): A tuple (u, v) representing an edge in the graph, where `u` and `v` are node IDs.
        degrees (dict): A dictionary mapping node IDs to their respective degrees in the graph.
        rule (dict): A dictionary representing the filtering rule. The rule should have a key `"degree_sum"`, 
                     which specifies the required sum of the degrees of the two nodes connected by the edge.

    Returns:
        bool: `True` if the sum of the degrees of the nodes connected by the edge equals the value 
              specified in `rule["degree_sum"]`, otherwise `False`.

    Example:
        >>> degrees = {1: 3, 2: 4, 3: 5}
        >>> edge = (1, 2)
        >>> rule = {"degree_sum": 7}
        >>> matches_rule(edge, degrees, rule)
        True

        >>> edge = (1, 3)
        >>> rule = {"degree_sum": 10}
        >>> matches_rule(edge, degrees, rule)
        False
    """
    u, v = edge
    deg_sum = degrees[u] + degrees[v]
    return deg_sum == rule["degree_sum"]

def count_matching_edges(G, rule):
    """
    Counts the number of edges in the graph G that satisfy a given filtering rule.

    Args:
        G (networkx.Graph): The graph to be analyzed.
        rule (dict): A dictionary representing the filtering rule. Must contain at least a "degree_sum" key.

    Returns:
        int: The number of edges that satisfy the rule.
    """
    degrees = dict(G.degree())
    count = 0
    for edge in G.edges():
        if matches_rule(edge, degrees, rule):
            count += 1
    return count

def satisfies_all_rules(G, rules):
    """
    Checks whether a graph G satisfies all the given filtering rules.

    Each rule is a dictionary with the following keys:
        - "degree_sum" (int): The sum of degrees to check for each edge.
        - "type" (str): The rule type — one of "min", "max", or "exactly".
        - "count" (int): The number of matching edges required by the rule.

    The function counts how many edges in G have the specified degree sum,
    and compares the count according to the rule's type:
        - "min": Requires at least 'count' matching edges.
        - "max": Allows at most 'count' matching edges.
        - "exactly": Requires exactly 'count' matching edges.

    Args:
        G (networkx.Graph): The input graph to evaluate.
        rules (list): A list of rule dictionaries.

    Returns:
        bool: True if all rules are satisfied, False otherwise.

    Example rule:
        {"degree_sum": 6, "type": "min", "count": 3}
        -> at least 3 edges must have endpoints whose degree sum is 6
    """
    for rule in rules:
        count = count_matching_edges(G, rule)
        if rule["type"] == "min" and count < rule["count"]:
            return False
        elif rule["type"] == "max" and count > rule["count"]:
            return False
        elif rule["type"] == "exactly" and count != rule["count"]:
            return False
    return True

def parse_args():
    """
    Parses command line arguments to allow the user to specify filter string,
    export options (image folder and format), and other flags.
    """
    parser = argparse.ArgumentParser(description='Filter graphs and optionally export images.')
    
    # Optional arguments for exporting images
    parser.add_argument('filter_string', type=str, help="The filter string in JSON format.")
    parser.add_argument('--export', metavar='FOLDER', type=str, help="Export filtered graphs as images to the specified folder.")
    parser.add_argument('--image', metavar='FORMAT', type=str, choices=['png', 'jpg', 'svg'], help="The image format for export.")
    
    return parser.parse_args()

def main():
    """
    Main entry point of the script.
    """
    args = parse_args()
    
    if args.export and not args.image:
        print("Error: You must specify an image format using --image (e.g., png, jpg, svg).")
        sys.exit(1)

    filter_str = args.filter_string
    rules = parse_rules(filter_str)

    input_count = 0
    output_count = 0
    passed_graphs = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        input_count += 1
        G = nx.from_graph6_bytes(line.encode())
        
        if satisfies_all_rules(G, rules):
            print(line)
            output_count += 1
            passed_graphs.append(line)
            
            if args.export:
                # Export the image directly to the folder provided after --export
                export_graph_image(line, args.image, args.export)

    # Optionally save history after processing
    # history_entry = HistoryEntry(...)
    # save_history([history_entry])

if __name__ == "__main__":
    main()