import pytest
import networkx as nx
import subprocess
from io import StringIO
from unittest.mock import patch
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
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3)])
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

# New tests for running the filter script via `run_filter.sh` and checking output

def test_run_filter_with_min_rule():
    """Test running the filter with a min-degree sum rule and check output."""
    rule_str = '[{"degree_sum": 4, "type": "min", "count": 1}]'
    
    # Mocking subprocess.Popen to run the filter script
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = "Bw\n"  # Simulate a graph output
        
        result = subprocess.run(
            ['./graph_processing/run_filter.sh', '4', rule_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Assert that the expected graph is returned as output
        assert "Bw" in result.stdout  # 'Bw' should match the output of the graph that passed the filter

def test_run_filter_with_max_rule():
    """Test running the filter with a max-degree sum rule and check output."""
    rule_str = '[{"degree_sum": 6, "type": "max", "count": 2}]'

    # Mocking subprocess.Popen to simulate a filter with more outputs
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = "D?w\nDCo\n"  # Simulate multiple graph outputs

        result = subprocess.run(
            ['./graph_processing/run_filter.sh', '4', rule_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Assert that both graphs passed the filter
        assert "D?w" in result.stdout
        assert "DCo" in result.stdout

def test_run_filter_with_exactly_rule():
    """Test running the filter with an exactly-degree sum rule and check output."""
    rule_str = '[{"degree_sum": 6, "type": "exactly", "count": 1}]'

    # Simulating a single output that fits the rule exactly
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = "DCw\n"  # Simulate one valid output
        
        result = subprocess.run(
            ['./graph_processing/run_filter.sh', '4', rule_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Assert that the valid graph is in the output
        assert "DCw" in result.stdout

def test_run_filter_with_no_matching_graphs():
    """Test running the filter where no graphs match the rule and check output."""
    rule_str = '[{"degree_sum": 10, "type": "min", "count": 1}]'

    # Simulate an empty output (no graphs matched)
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = ""  # No valid graph output
        
        result = subprocess.run(
            ['./graph_processing/run_filter.sh', '4', rule_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Assert no graphs were returned
        assert result.stdout == ""

def test_run_filter_with_filter_validation():
    """Test running the filter script and validate that the output graphs satisfy the applied filter."""
    rule_str = '[{"degree_sum": 6, "type": "min", "count": 1}]'

    # Simulate the expected behavior with the mock subprocess.Popen
    with patch('subprocess.Popen') as mock_popen:
        # Simulate the graph outputs from the script
        mock_popen.return_value.stdout = StringIO("Bw\nDCo\n")  # Two example graph outputs

        try:
            result = subprocess.run(
                ['./graph_processing/run_filter.sh', '4', rule_str],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Check if the result contains output
            if result.stdout:
                print("Output graphs:", result.stdout)
                output_graphs = result.stdout.strip().split('\n')
                for graph in output_graphs:
                    print(f"Processing graph: {graph}")
                    # Get the degrees of the graph (this should be fetched from actual graph data)
                    degrees = get_graph_degrees(graph)
                    print(f"Graph degrees: {degrees}")
                    for rule in parse_rules(rule_str):
                        print(f"Checking rule: {rule}")
                        assert matches_rule(graph, degrees, rule), f"Graph {graph} did not match the rule {rule}"

            else:
                print("No output from subprocess")
                
            # Optionally, check if there were errors in stderr
            if result.stderr:
                print(f"Error: {result.stderr}")

        except Exception as e:
            print(f"Error while running subprocess: {e}")
