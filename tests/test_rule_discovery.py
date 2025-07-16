import unittest
from pathlib import Path
import sys
sys.path.append('/Users/cblank/src/the-company-os/os/domains/rules_service/src')
sys.path.append('/Users/cblank/src/the-company-os/shared/libraries')
from discovery import RuleDiscoveryService

class TestRuleDiscovery(unittest.TestCase):

    def setUp(self):
        self.root_path = Path('/Users/cblank/src/the-company-os')
        self.discovery_service = RuleDiscoveryService(self.root_path)

    def test_discover_rules(self):
        rules = self.discovery_service.discover_rules()
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        print(f"Discovered {len(rules)} rule files.")

    def test_query_by_tags(self):
        rules = self.discovery_service.query_by_tags(["validation"])
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        print(f"Found {len(rules)} rules with tag 'validation'.")
        for rule in rules:
            self.assertIn("validation", rule.tags)

if __name__ == '__main__':
    unittest.main()