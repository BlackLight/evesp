import os
import unittest

from evesp.event import Event, AttributeValueAny
from evesp.rules_parser import RulesParser

class TestRulesParser(unittest.TestCase):
    def setUp(self):
        basedir = os.path.dirname(os.path.realpath(__file__))
        rules = os.path.join(basedir, 'rules', 'test_mock_component_rules.json')
        self.rules = RulesParser(rules).get_rules()

    def test_rules_number(self):
        self.assertEqual(len(self.rules), 1)

    def test_rules_label(self):
        self.assertEqual(self.rules[0]['label'], 'Test rule 1')

    def test_rules_events(self):
        events = self.rules[0]['when']
        self.assertEqual(len(events), 1)

        event = events[0]
        self.assertEqual(event.id, 1)
        self.assertTrue(isinstance(event.name, AttributeValueAny))

    def test_rules_actions(self):
        actions = self.rules[0]['then']
        self.assertEqual(len(actions), 1)

        action = actions[0]
        self.assertEqual(action.filepath, 'tests/events.bin')

if __name__ == "__main__":
    unittest.main()

# vim:sw=4:ts=4:et:

