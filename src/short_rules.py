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
    def __init__(self, fst, snd, dec=None):
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
    def __init__(self, fst, snd, cons, dec=None):
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


class Sequence:
    def __init__(self, nt, empty_obj, cons):
        self._nt = nt
        self._empty_obj = empty_obj
        self._cons = cons

    def _to_std_rules(self, name=None):
        if name is None:
            name = get_id()
        seq_rule = Union(
            Epsilon(self._empty_obj),
            Prod(NonTerm(name), self._nt, self._cons),
            lambda obj: obj == self._empty_obj,
        )
        return seq_rule._to_std_rules(name)


def to_std_grammar(short_grammar):
    rules = []
    for nt, short_rule in short_grammar.items():
        rules += short_rule._to_std_rules(nt)
    return {k: v for k, v in rules if v is not None}
