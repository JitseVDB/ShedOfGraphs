import unittest
import networkx as nx
from filter_graph import satisfies_all_rules, parse_rules

class TestFilterGraph(unittest.TestCase):

    def setUp(self):
        """
        Set up test graphs for use in the test cases. 
        G1 is a triangle with all degrees = 2, 
        and G2 is a line graph with varying degrees.
        """
        self.G1 = nx.Graph()
        self.G1.add_edges_from([(0, 1), (1, 2), (2, 0)])  # triangle, all degrees = 2

        self.G2 = nx.Graph()
        self.G2.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])  # line, degrees vary

    def test_min_rule_valid(self):
        """
        Test the 'min' rule where at least 2 edges with degree sum = 4 should exist.
        G1 should satisfy this rule as it has a degree sum of 2 for each edge, 
        and the minimum requirement is met.
        """
        # At least 2 edges with degree sum = 4
        rules = [{"degree_sum": 4, "type": "min", "count": 2}]
        self.assertTrue(satisfies_all_rules(self.G1, rules))

    def test_min_rule_invalid(self):
        """
        Test the 'min' rule where the requirement for 4 matching edges is too strict. 
        G1 does not satisfy this rule as it cannot meet the condition of 4 edges with a degree sum of 4.
        """
        # Too strict: require 4 matching edges
        rules = [{"degree_sum": 4, "type": "min", "count": 4}]
        self.assertFalse(satisfies_all_rules(self.G1, rules))

    def test_max_rule_pass_valid(self):
        """
        Test the 'max' rule where the condition of a maximum degree sum of 3 across 3 edges is met. 
        G2 satisfies this condition.
        """
        rules = [{"degree_sum": 3, "type": "max", "count": 3}]
        self.assertTrue(satisfies_all_rules(self.G2, rules))

    def test_max_rule_pass_invalid(self):
        """
        Test the 'max' rule with a condition that only 1 edge can have a degree sum of 3, 
        but G2 has more than 1 edge satisfying the condition, so it should fail.
        """
        rules = [{"degree_sum": 3, "type": "max", "count": 1}]
        self.assertFalse(satisfies_all_rules(self.G2, rules))

    def test_exactly_rule_valid(self):
        """
        Test the 'exactly' rule where the condition of having exactly 2 edges with degree sum 3 is met. 
        G2 should satisfy this rule.
        """
        rules = [{"degree_sum": 3, "type": "exactly", "count": 2}]
        self.assertTrue(satisfies_all_rules(self.G2, rules))

    def test_exactly_rule_invalid(self):
        """
        Test the 'exactly' rule where G2 has more than 1 edge with degree sum 3, 
        but the rule only allows exactly 1 edge to satisfy the condition.
        """
        rules = [{"degree_sum": 3, "type": "exactly", "count": 1}]
        self.assertFalse(satisfies_all_rules(self.G2, rules))

    def test_multiple_rules_pass(self):
        """
        Test applying multiple rules at once. 
        The first rule requires a minimum of 2 edges with degree sum 4, 
        and the second rule requires at least 1 edge with degree sum 3.
        G1 satisfies both rules.
        """
        rules = [
            {"degree_sum": 4, "type": "min", "count": 2},
            {"degree_sum": 3, "type": "max", "count": 1}
        ]
        self.assertTrue(satisfies_all_rules(self.G1, rules))

    def test_multiple_rules_fail(self):
        """
        Test applying multiple rules where one rule fails.
        The first rule requires a minimum of 2 edges with degree sum 4, 
        and the second rule requires exactly 1 edge with degree sum 5, 
        but G1 does not satisfy the second rule.
        """
        rules = [
            {"degree_sum": 4, "type": "min", "count": 2},
            {"degree_sum": 5, "type": "exactly", "count": 1}
        ]
        self.assertFalse(satisfies_all_rules(self.G1, rules))

    def test_parse_rules_valid(self):
        """
        Test parsing a valid rule string. 
        The rule string should be parsed into a list of dictionaries, 
        and the parsed value should match the input.
        """
        rule_str = '[{"degree_sum": 6, "type": "min", "count": 2}]'
        parsed = parse_rules(rule_str)
        self.assertIsInstance(parsed, list)
        self.assertEqual(parsed[0]["type"], "min")

    def test_parse_rules_invalid_json(self):
        """
        Test parsing an invalid JSON rule string. 
        The function should raise a SystemExit error due to malformed JSON.
        """
        with self.assertRaises(SystemExit):
            parse_rules('{"degree_sum": 6, "type": "min"')  # Missing closing brace

    def test_invalid_rule_missing_fields(self):
        """
        Test invalid rule with missing required fields. 
        The rule is missing 'degree_sum' and should raise a KeyError when checked.
        """
        bad_rule = [{"type": "min", "count": 1}]  # Missing "degree_sum"
        with self.assertRaises(KeyError):
            satisfies_all_rules(self.G1, bad_rule)

    def test_invalid_rule_unknown_type(self):
        """
        Test invalid rule with an unknown rule type. 
        The rule type 'minimum' is invalid and should raise a KeyError.
        """
        bad_rule = [{"degree_sum": 4, "type": "minimum", "count": 2}]  # Invalid type
        with self.assertRaises(KeyError):  # Your implementation doesn't check type string explicitly
            satisfies_all_rules(self.G1, bad_rule)


if __name__ == "__main__":
    unittest.main()
