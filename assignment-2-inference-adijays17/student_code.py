import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Student code goes here
        ####################################################
        if factq(fact_or_rule):
            if fact_or_rule in self.facts :
                ind = self.facts.index(fact_or_rule)
                factToBeRemoved = self.facts[ind]
                if len(factToBeRemoved.supported_by) == 0:
                    self.facts.pop(ind) 
                    self.adjust_supported_by_fact(factToBeRemoved)                                       
                    for eachFact in factToBeRemoved.supports_facts :
                        self.removing_infered_facts(eachFact)
                    for eachRule in factToBeRemoved.supports_rules:
                        self.removing_infered_rules(eachRule)
                else:
                    if factToBeRemoved.asserted :
                        factToBeRemoved.asserted = False
                    
    def removing_infered_facts(self, removingFact):
        if factq(removingFact):
            if removingFact in self.facts :
                ind = self.facts.index(removingFact)
                factToBeRemoved = self.facts[ind]
                if len(factToBeRemoved.supported_by) == 0 and not factToBeRemoved.asserted:
                    self.adjust_supported_by_fact(factToBeRemoved)
                    self.facts.pop(ind)                    
                    for eachFact in factToBeRemoved.supports_facts :
                        self.removing_infered_facts(eachFact)
                    for eachRule in factToBeRemoved.supports_rules:
                        self.removing_infered_rules(eachRule)
                    
    def removing_infered_rules(self, rule):
        if not rule.asserted and rule in self.rules :
            ind = self.rules.index(rule)
            rulesToBeRemoved = self.rules[ind]
            if len(rulesToBeRemoved.supported_by) == 0:
                self.adjust_supported_by_rule(rulesToBeRemoved)
                self.rules.pop(ind)
                for eachFact in rule.supports_facts :
                    self.removing_infered_facts(eachFact)
                for eachRule in rule.supports_rules:
                    self.removing_infered_rules(eachRule)
                
                
    def adjust_supported_by_fact(self, removedFact):
        for eachFact in self.facts:
            for supportedBy in eachFact.supported_by:
                if removedFact == supportedBy[0]:
                    indexOfSupportedByToBeRemoved = eachFact.supported_by.index(supportedBy)
                    eachFact.supported_by.pop(indexOfSupportedByToBeRemoved)
        for eachRule in self.rules:
            for supportedBy in eachRule.supported_by:
                if removedFact == supportedBy[0]:
                    indexOfSupportedByToBeRemoved = eachRule.supported_by.index(supportedBy)
                    eachRule.supported_by.pop(indexOfSupportedByToBeRemoved)
    
    def adjust_supported_by_rule(self, removedRule):
        for eachFact in self.facts:
            for supportedBy in eachFact.supported_by:
                if removedRule == supportedBy[1]:
                    indexOfSupportedByToBeRemoved = eachFact.supported_by.index(supportedBy)
                    eachFact.supported_by.pop(indexOfSupportedByToBeRemoved)
        for eachRule in self.rules:
            for supportedBy in eachRule.supported_by:
                if removedRule == supportedBy[1]:
                    indexOfSupportedByToBeRemoved = eachRule.supported_by.index(supportedBy)
                    eachRule.supported_by.pop(indexOfSupportedByToBeRemoved)        

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        #
        # Below FC Algorithm implemented taught in class  
        #
        # Get first statement in lhs of rule
        # Unify fact with first statement
        #    If substitution found
        #        If lhs is only one statement
        #            Create new fact using the substitution on rhs
        #            Add new fact to kb
        #        Else
        #            Create new rule with rest of lhs and rhs
        #            Add new rule to kb
        #####################################################       
        lhsStatement = rule.lhs[0]   
        associatedBindings = match(lhsStatement, fact.statement)
        if associatedBindings:  
            variableReplacedBinding = instantiate(rule.rhs, associatedBindings)
            if len(rule.lhs) == 1:
                newfact = Fact(variableReplacedBinding, [[fact, rule]])
                fact.supports_facts.append(newfact)
                rule.supports_facts.append(newfact)
                kb.kb_add(newfact)
            else:
                lhs = []
                for eachlhs in rule.lhs[1:]:
                    lhs.append(instantiate(eachlhs, associatedBindings))
                newRule = Rule([lhs, variableReplacedBinding], [[fact, rule]])
                fact.supports_rules.append(newRule)
                rule.supports_rules.append(newRule)
                kb.kb_add(newRule)