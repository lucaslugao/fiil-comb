from grammars import grammars
from rules import init_grammar

N_MAX = 10

for grammar in grammars.values():
    init_grammar(grammar)
    for rule in grammar.values():
        for n in range(0, N_MAX):
            assert rule.list(n) == [rule.unrank(n, i) for i in range(0, rule.count(n))]
            assert all([rule.rank(obj) == i for i, obj in enumerate(rule.list(n))])

