import inspect
import json
from evesp.utils import *

class RulesParsingError(Exception):
    pass

class RulesParser(object):
    """
    Rules parser
    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    def __init__(self, rules_file):
        self.__rules_file = rules_file
        with open(self.__rules_file) as fp:
            self.__root = json.load(fp)
        self.__parse_rules()

    def __parse_rules(self):
        self.__rules = []
        self.__rules_by_event_class = {}

        for rule in self.__root:
            self.__rules.append(
                self.__rule_from_json(rule, len(self.__rules)+1)
            )

    def __event_from_json(self, event):
        if not 'class' in event:
            event['class'] = 'Event'
        return event

    def __rule_from_json(self, rule, rule_idx):
        self.__parse_rule_when_attribute(rule, rule_idx)
        self.__parse_rule_then_attribute(rule, rule_idx)
        return rule

    def __parse_rule_when_attribute(self, rule, rule_idx):
        from evesp.event import Event, AttributeValueAny

        if not 'when' in rule:
            raise RulesParsingError('Rule #%d has no "when" attribute' % rule_idx)

        if not isinstance(rule['when'], list):
            raise RulesParsingError('Expected [list] for rule #%d when attribute, got [%s]'
                % (rule_idx, type(rule['when']).__name__))

        events = []
        for event in rule['when']:
            event_class = event_class_by_class_name(event['class'] or 'Event')
            event_attributes = list(inspect.signature(event_class.__init__).parameters.keys())
            event_attributes.pop(0)  # Remove self
            filter_attributes = event['attributes'] if 'attributes' in event else {}

            for attr in event_attributes:
                if not attr in filter_attributes:
                    filter_attributes[attr] = AttributeValueAny()
            events.append(event_class(**(filter_attributes)))

        rule['when'] = events
        return rule

    def __parse_rule_then_attribute(self, rule, rule_idx):
        if not 'then' in rule:
            raise RulesParsingError('Rule #%d has no "then" attribute' % rule_idx)

        if not isinstance(rule['then'], list):
            raise RulesParsingError('Expected [list] for rule #%d then attribute, got [%s]'
                % (rule_idx, type(rule['then']).__name__))

        actions = []
        for action in rule['then']:
            actuator_class = actuator_class_by_class_name(action['class'] or 'Actuator')
            actuator_attributes = list(inspect.signature(actuator_class.__init__).parameters.keys())
            actuator_attributes.pop(0)  # Remove self
            init_arguments = action['arguments'] if 'arguments' in action else {}
            actions.append(actuator_class(**(init_arguments)))

        rule['then'] = actions
        return rule

    def get_rules(self):
        """
        Get the list of parsed rules
        """
        return self.__rules

# vim:sw=4:ts=4:et:
