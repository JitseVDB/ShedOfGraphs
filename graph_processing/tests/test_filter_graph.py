import pytest
import networkx as nx
from graph_processing.filter_graph import (
    parse_rules,
    satisfies_all_rules,
    count_matching_edges,
    matches_rule
)

def test_parse_rules_valid():
    """Test that valid JSON rule strings are parsed correctly."""
    rule_str = '[{"degree_sum": 6, "type": "min", "count": 2}]'
    expected = [{"degree_sum": 6, "type": "min", "count": 2}]
    assert parse_rules(rule_str) == expected

def test_parse_rules_invalid_json():
    """Test that invalid JSON input causes the program to exit."""
    rule_str = '[{"degree_sum": 6, "type": "min", "count":}]'
    with pytest.raises(SystemExit):
        parse_rules(rule_str)

def test_matches_rule_valid():
    """Test that an edge satisfying the degree_sum rule returns True."""
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    degrees = {0: 2, 1: 3, 2: 2}
    rule = {"degree_sum": 5}
    assert matches_rule((0, 1), degrees, rule)

def test_matches_rule_invalid():
    """Test that an edge not satisfying the degree_sum rule returns False."""
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    degrees = {0: 2, 1: 3, 2: 2}
    rule = {"degree_sum": 6}
    assert not matches_rule((0, 1), degrees, rule)

def test_satisfies_all_rules_valid():
    """Test that a graph satisfying the minimum number of matching edges passes."""
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])
    rule = {"degree_sum": 5, "type": "min", "count": 2}
    assert satisfies_all_rules(G, [rule])

def test_satisfies_all_rules_invalid():
    """Test that a graph not satisfying the minimum number of matching edges fails."""
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rule = {"degree_sum": 6, "type": "min", "count": 2}
    assert not satisfies_all_rules(G, [rule])

def test_empty_graph():
    """Test that an empty graph does not satisfy any rule."""
    G = nx.Graph()
    rule = {"degree_sum": 6, "type": "min", "count": 2}
    assert not satisfies_all_rules(G, [rule])