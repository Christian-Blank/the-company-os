import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent / 'os/domains/rules_service/src'))
sys.path.append(str(Path(__file__).parent.parent / 'shared/libraries'))
from discovery import RuleDiscoveryService

class TestRuleDiscovery(unittest.TestCase):

    def setUp(self):
        self.root_path = Path('/Users/cblank/src/the-company-os')
        self.discovery_service = RuleDiscoveryService(self.root_path)

    def test_discover_rules(self):
        rules, errors = self.discovery_service.discover_rules()
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        self.assertEqual(len(errors), 0)
        print(f"Discovered {len(rules)} rule files.")

    def test_query_by_tags(self):
        rules = self.discovery_service.query_by_tags(["validation"])
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        print(f"Found {len(rules)} rules with tag 'validation'.")
        for rule in rules:
            self.assertIn("validation", rule.tags)

    def test_rule_category(self):
        rules, _ = self.discovery_service.discover_rules()
        for rule in rules:
            self.assertIsInstance(rule.rule_category, str)
            self.assertNotEqual(rule.rule_category, "uncategorized")
            print(f"Rule {rule.title} has category: {rule.rule_category}")

    def test_query_with_pagination(self):
        rules = self.discovery_service.query_by_tags(["rules"], limit=2, offset=1, sort_by='title')
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0].title, "Rule Set: The Decision System")

if __name__ == '__main__':
    unittest.main()