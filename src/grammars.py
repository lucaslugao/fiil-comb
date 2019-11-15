from rules import *
from itertools import accumulate

treeGram = {
    "Tree": UnionRule("Node", "Leaf"),
    "Node": ProductRule("Tree", "Tree", lambda a: "Node({},{})".format(*a)),
    "Leaf": SingletonRule("Leaf"),
}

fiboGram = {
    "Fib": UnionRule("Vide", "Cas1"),
    "Cas1": UnionRule("CasAu", "Cas2"),
    "Cas2": UnionRule("AtomB", "CasBAu"),
    "Vide": EpsilonRule(""),
    "CasAu": ProductRule("AtomA", "Fib", "".join),
    "AtomA": SingletonRule("A"),
    "AtomB": SingletonRule("B"),
    "CasBAu": ProductRule("AtomB", "CasAu", "".join),
}

abGram = {
    "E": EpsilonRule(""),
    "A": SingletonRule("A"),
    "B": SingletonRule("B"),
    "W": UnionRule("AW|BW", "E", lambda obj: len(obj) > 0),
    "AW": ProductRule("A", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "BW": ProductRule("B", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "AW|BW": UnionRule("AW", "BW", lambda obj: obj[0] == "A"),
}


def split_on_acc(obj, add_on="A", cut_val=1):
    n = 0
    for i, e in enumerate(obj):
        n += 1 if e == add_on else -1
        if n == cut_val:
            return (obj[: i + 1], obj[i + 1 :])


dyckGram = {
    "E": EpsilonRule(""),
    "(": SingletonRule("("),
    ")": SingletonRule(")"),
    "W": UnionRule("E", "(W)W", lambda obj: len(obj) == 0),
    "(W)W": ProductRule("(W)", "W", "".join, lambda obj: split_on_acc(obj, "(", 0)),
    "(W)": ProductRule("(W", ")", "".join, lambda obj: (obj[:-1], obj[-1])),
    "(W": ProductRule("(", "W", "".join, lambda obj: (obj[0], obj[1:])),
}

max3Gram = {
    "E": EpsilonRule(""),
    "A": SingletonRule("A"),
    "B": SingletonRule("B"),
    "W": UnionRule("E", "A1|B1", lambda obj: len(obj) == 0),
    "A1": ProductRule("A", "E|A2|B1", "".join, lambda obj: (obj[0], obj[1:])),
    "B1": ProductRule("B", "E|B2|A1", "".join, lambda obj: (obj[0], obj[1:])),
    "A2": ProductRule("A", "E|B1", "".join, lambda obj: (obj[0], obj[1:])),
    "B2": ProductRule("B", "E|A1", "".join, lambda obj: (obj[0], obj[1:])),
    "E|A2|B1": UnionRule("E", "A2|B1", lambda obj: len(obj) == 0),
    "E|B2|A1": UnionRule("E", "B2|A1", lambda obj: len(obj) == 0),
    "A2|B1": UnionRule("A2", "B1", lambda obj: obj[0] == "A"),
    "B2|A1": UnionRule("B2", "A1", lambda obj: obj[0] == "B"),
    "A1|B1": UnionRule("A1", "B1", lambda obj: obj[0] == "A"),
    "E|B1": UnionRule("E", "B1", lambda obj: len(obj) == 0),
    "E|A1": UnionRule("E", "A1", lambda obj: len(obj) == 0),
}

abPalindromeGram = {
    "E": EpsilonRule(""),
    "A": SingletonRule("A"),
    "B": SingletonRule("B"),
    "W": UnionRule("E", "A|B|AWA|BWB", lambda obj: len(obj) == 0),
    "A|B|AWA|BWB": UnionRule("A", "B|AWA|BWB", lambda obj: obj == "A"),
    "B|AWA|BWB": UnionRule("B", "AWA|BWB", lambda obj: obj == "B"),
    "AWA|BWB": UnionRule("AWA", "BWB", lambda obj: obj[0] == "A"),
    "AW": ProductRule("A", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "AWA": ProductRule("AW", "A", "".join, lambda obj: (obj[:-1], obj[-1])),
    "BW": ProductRule("B", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "BWB": ProductRule("BW", "B", "".join, lambda obj: (obj[:-1], obj[-1])),
}

abcPalindromeGram = {
    "E": EpsilonRule(""),
    "A": SingletonRule("A"),
    "B": SingletonRule("B"),
    "C": SingletonRule("C"),
    "W": UnionRule("E", "A|B|C|AWA|BWB|CWC", lambda obj: len(obj) == 0),
    "A|B|C|AWA|BWB|CWC": UnionRule("A", "B|C|AWA|BWB|CWC", lambda obj: obj == "A"),
    "B|C|AWA|BWB|CWC": UnionRule("B", "C|AWA|BWB|CWC", lambda obj: obj == "B"),
    "C|AWA|BWB|CWC": UnionRule("C", "AWA|BWB|CWC", lambda obj: obj == "C"),
    "AWA|BWB|CWC": UnionRule("AWA", "BWB|CWC", lambda obj: obj[0] == "A"),
    "BWB|CWC": UnionRule("BWB", "CWC", lambda obj: obj[0] == "B"),
    "AW": ProductRule("A", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "AWA": ProductRule("AW", "A", "".join, lambda obj: (obj[:-1], obj[-1])),
    "BW": ProductRule("B", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "BWB": ProductRule("BW", "B", "".join, lambda obj: (obj[:-1], obj[-1])),
    "CW": ProductRule("C", "W", "".join, lambda obj: (obj[0], obj[1:])),
    "CWC": ProductRule("CW", "C", "".join, lambda obj: (obj[:-1], obj[-1])),
}


abEqualCountGram = {
    "E": EpsilonRule(""),
    "A": SingletonRule("A"),
    "B": SingletonRule("B"),
    "W": UnionRule("AbW|BaW", "E", lambda obj: len(obj) > 0),
    "a": UnionRule("A", "Baa", lambda obj: obj == "A"),
    "b": UnionRule("B", "Abb", lambda obj: obj == "B"),
    "AbW|BaW": UnionRule("AbW", "BaW", lambda obj: obj[0] == "A"),
    "AbW": ProductRule("A", "bW", "".join, lambda obj: (obj[0], obj[1:])),
    "Abb": ProductRule("A", "bb", "".join, lambda obj: (obj[0], obj[1:])),
    "Baa": ProductRule("B", "aa", "".join, lambda obj: (obj[0], obj[1:])),
    "BaW": ProductRule("B", "aW", "".join, lambda obj: (obj[0], obj[1:])),
    "bW": ProductRule("b", "W", "".join, lambda obj: split_on_acc(obj, "B", 1)),
    "aW": ProductRule("a", "W", "".join, lambda obj: split_on_acc(obj, "A", 1)),
    "aa": ProductRule("a", "a", "".join, lambda obj: split_on_acc(obj, "A", 1)),
    "bb": ProductRule("b", "b", "".join, lambda obj: split_on_acc(obj, "B", 1)),
}

grammars = {
    grammar_name: grammar
    for grammar_name, grammar in globals().items()
    if "Gram" in grammar_name
}
