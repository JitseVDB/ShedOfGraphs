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

import sys
import json
import networkx as nx

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

def main():
    if len(sys.argv) != 2:
        print("Usage: python filter_graph.py '<filter_string>'")
        sys.exit(1)

    filter_str = sys.argv[1]
    rules = parse_rules(filter_str)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        G = nx.from_graph6_bytes(line.encode())
        if satisfies_all_rules(G, rules):
            print(line)

if __name__ == "__main__":
    main()
