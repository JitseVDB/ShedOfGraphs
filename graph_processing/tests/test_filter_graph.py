import unittest
import networkx as nx
from filter_graph import satisfies_all_rules, parse_rules

class TestFilterGraph(unittest.TestCase):

    def setUp(self):
        # Create test graphs
        self.G1 = nx.Graph()
        self.G1.add_edges_from([(0, 1), (1, 2), (2, 0)])  # triangle, all degrees = 2

        self.G2 = nx.Graph()
        self.G2.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])  # line, degrees vary

    def test_min_rule_valid(self):
        # At least 2 edges with degree sum = 4
        rules = [{"degree_sum": 4, "type": "min", "count": 2}]
        self.assertTrue(satisfies_all_rules(self.G1, rules))

    def test_min_rule_invalid(self):
        # Too strict: require 4 matching edges
        rules = [{"degree_sum": 4, "type": "min", "count": 4}]
        self.assertFalse(satisfies_all_rules(self.G1, rules))

    def test_max_rule_pass_valid(self):
        rules = [{"degree_sum": 3, "type": "max", "count": 3}]
        self.assertTrue(satisfies_all_rules(self.G2, rules))

    def test_max_rule_pass_invalid(self):
        rules = [{"degree_sum": 3, "type": "max", "count": 1}]
        self.assertFalse(satisfies_all_rules(self.G2, rules))

    def test_exactly_rule_valid(self):
        rules = [{"degree_sum": 3, "type": "exactly", "count": 2}]
        self.assertTrue(satisfies_all_rules(self.G2, rules))

    def test_exactly_rule_invalid(self):
        rules = [{"degree_sum": 3, "type": "exactly", "count": 1}]
        self.assertFalse(satisfies_all_rules(self.G2, rules))

    def test_multiple_rules_pass(self):
        rules = [
            {"degree_sum": 4, "type": "min", "count": 2},
            {"degree_sum": 3, "type": "max", "count": 1}
        ]
        self.assertTrue(satisfies_all_rules(self.G1, rules))

    def test_multiple_rules_fail(self):
        rules = [
            {"degree_sum": 4, "type": "min", "count": 2},
            {"degree_sum": 5, "type": "exactly", "count": 1}
        ]
        self.assertFalse(satisfies_all_rules(self.G1, rules))

    def test_parse_rules_valid(self):
        rule_str = '[{"degree_sum": 6, "type": "min", "count": 2}]'
        parsed = parse_rules(rule_str)
        self.assertIsInstance(parsed, list)
        self.assertEqual(parsed[0]["type"], "min")

    def test_parse_rules_invalid_json(self):
        with self.assertRaises(SystemExit):
            parse_rules('{"degree_sum": 6, "type": "min"')  # Missing closing brace

    def test_invalid_rule_missing_fields(self):
        bad_rule = [{"type": "min", "count": 1}]  # Missing "degree_sum"
        with self.assertRaises(KeyError):
            satisfies_all_rules(self.G1, bad_rule)

    def test_invalid_rule_unknown_type(self):
        bad_rule = [{"degree_sum": 4, "type": "minimum", "count": 2}]  # Invalid type
        with self.assertRaises(KeyError):  # Your implementation doesn't check type string explicitly
            satisfies_all_rules(self.G1, bad_rule)


if __name__ == "__main__":
    unittest.main()
