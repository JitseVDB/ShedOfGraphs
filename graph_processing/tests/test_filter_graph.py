import networkx as nx
from graph_processing.filter_graph import satisfies_all_rules

def test_satisfies_min_rule():
    """
    Test the 'min' rule type in the filtering logic.

    This test creates a graph with four nodes and four edges, where:
        - Node 0 is connected to Node 1
        - Node 1 is connected to Node 2
        - Node 2 is connected to Node 3
        - Node 3 is connected back to Node 0

    The rule being tested requires that at least 2 edges should have their degree sum equal to 2.
    This is expected to pass because the sum of degrees of connected nodes in each edge matches the rule.

    Expected behavior:
        The function should return True, as the graph meets the rule.
    """
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

    rule = {"degree_sum": 2, "type": "min", "count": 2}
    assert satisfies_all_rules(G, [rule])  # Should pass


def test_satisfies_exactly_rule():
    """
    Test the 'exactly' rule type in the filtering logic.

    This test creates a simple path graph with 3 nodes (0-1-2), where:
        - Node 0 is connected to Node 1
        - Node 1 is connected to Node 2

    The rule being tested requires exactly 2 edges where the sum of the degrees of the connected nodes equals 3.
    This is expected to pass because the sum of degrees for both edges is exactly 3.

    Expected behavior:
        The function should return True, as the graph meets the rule.
    """
    G = nx.path_graph(3)  # 0-1-2

    rule = {"degree_sum": 3, "type": "exactly", "count": 2}
    assert satisfies_all_rules(G, [rule])  # Should pass


def test_invalid_rule_type():
    """
    Test invalid rule types in the filtering logic.

    This test creates a complete graph with 3 nodes, where:
        - All nodes are connected to each other (3 nodes and 3 edges).

    The rule being tested uses an unsupported rule type (`"unsupported"`), which should raise a KeyError.

    Expected behavior:
        The function should raise a KeyError because the rule type is not recognized.
    """
    G = nx.complete_graph(3)

    rule = {"degree_sum": 4, "type": "unsupported", "count": 1}
    try:
        satisfies_all_rules(G, [rule])
    except KeyError:
        assert True  # Test passed: the function raised the expected exception
    else:
        assert False, "Should have raised an error"  # Test failed if no exception is raised