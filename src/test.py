from grammars import grammars
from rules import init_grammar

N_MAX = 10

for grammar in grammars.values():
    init_grammar(grammar)
    for rule in grammar.values():
        for n in range(0, N_MAX):
            assert len(rule.list(n)) == rule.count(n)
            assert all([rule.unrank(n, i) == obj for i, obj in enumerate(rule.list(n))])
            assert all([len(el) == n for el in rule.list(n)])
            assert all([rule.rank(obj) == i for i, obj in enumerate(rule.list(n))])
            try:
                rule.unrank(n, rule.count(n) + 1)
                assert False
            except:
                pass
