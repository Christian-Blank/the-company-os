import unittest
from pathlib import Path
import sys
import os

from discovery import RuleDiscoveryService

class TestRuleDiscoveryEdgeCases(unittest.TestCase):

    def setUp(self):
        self.root_path = Path('/Users/cblank/src/the-company-os/tests/fixtures')
        self.discovery_service = RuleDiscoveryService(self.root_path)
        # Create dummy files for testing
        os.makedirs(self.root_path, exist_ok=True)
        with open(self.root_path / "malformed.rules.md", "w") as f:
            f.write("---\ntitle: Malformed\nversion: 1.0\nstatus: Active\nowner: Test\nlast_updated: 2025-07-16T00:00:00-07:00\nparent_charter: some/charter.md\n: broken yaml\n---")
        with open(self.root_path / "no_frontmatter.rules.md", "w") as f:
            f.write("No frontmatter here.")
        with open(self.root_path / "empty.rules.md", "w") as f:
            f.write("")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.root_path)

    def test_malformed_yaml(self):
        rules, errors = self.discovery_service.discover_rules()
        self.assertEqual(len(rules), 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("malformed.rules.md", errors[0])

    def test_no_frontmatter(self):
        # Re-initialize to clear cache
        self.discovery_service = RuleDiscoveryService(self.root_path)
        # Create a file with no frontmatter
        with open(self.root_path / "no_frontmatter.rules.md", "w") as f:
            f.write("No frontmatter here.")
        rules, errors = self.discovery_service.discover_rules()
        # This should not produce an error, just be skipped
        self.assertEqual(len(rules), 0)
        self.assertEqual(len(errors), 1)

    def test_empty_file(self):
        # Re-initialize to clear cache
        self.discovery_service = RuleDiscoveryService(self.root_path)
        # Create an empty file
        with open(self.root_path / "empty.rules.md", "w") as f:
            f.write("")
        rules, errors = self.discovery_service.discover_rules()
        self.assertEqual(len(rules), 0)
        self.assertEqual(len(errors), 1)

    def test_plus_delimiter(self):
        # Re-initialize to clear cache
        self.discovery_service = RuleDiscoveryService(self.root_path)
        # Create a file with '+++' delimiters
        with open(self.root_path / "plus_delimiter.rules.md", "w") as f:
            f.write("""+++
title: Plus Delimiter
version: 1.0
status: Active
owner: Test
last_updated: 2025-07-16T00:00:00-07:00
parent_charter: some/charter.md
+++""")
        rules, errors = self.discovery_service.discover_rules()
        self.assertEqual(len(rules), 1)
        self.assertEqual(len(errors), 1)

if __name__ == '__main__':
    unittest.main()