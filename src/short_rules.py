from rules import SingletonRule
from rules import EpsilonRule
from rules import UnionRule
from rules import ProductRule
from uuid import uuid4


def get_id():
    return "rule-{}".format(str(uuid4()).replace("-", ""))


class NonTerm:
    def __init__(self, name):
        self._name = name

    def _to_std_rules(self):
        return [(self._name, None)]


class Singleton:
    def __init__(self, obj):
        self._obj = obj

    def _to_std_rules(self, name=None):
        if name is None:
            name = get_id()
        return [(name, SingletonRule(self._obj))]


class Epsilon:
    def __init__(self, obj):
        self._obj = obj

    def _to_std_rules(self, name=None):
        if name is None:
            name = get_id()
        return [(name, EpsilonRule(self._obj))]


class Union:
    def __init__(self, fst, snd, dec):
        self._fst = fst
        self._snd = snd
        self._dec = dec

    def _to_std_rules(self, name=None):
        if name is None:
            name = get_id()
        fst_rules = self._fst._to_std_rules()
        snd_rules = self._snd._to_std_rules()
        return (
            [(name, UnionRule(fst_rules[0][0], snd_rules[0][0], self._dec))]
            + fst_rules
            + snd_rules
        )


class Prod:
    def __init__(self, fst, snd, cons, dec):
        self._fst = fst
        self._snd = snd
        self._cons = cons
        self._dec = dec

    def _to_std_rules(self, name=None):
        if name is None:
            name = get_id()
        fst_rules = self._fst._to_std_rules()
        snd_rules = self._snd._to_std_rules()
        return (
            [
                (
                    name,
                    ProductRule(
                        fst_rules[0][0], snd_rules[0][0], self._cons, self._dec
                    ),
                )
            ]
            + fst_rules
            + snd_rules
        )


def to_std_grammar(short_grammar):
    rules = []
    for nt, short_rule in short_grammar.items():
        rules += short_rule._to_std_rules(nt)
    return {k: v for k, v in rules if v is not None}
