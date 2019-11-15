from abc import ABC, abstractmethod
import random
import functools


class AbstractRule(ABC):
    def __init__(self):
        self.valuation = float("inf")
        self._count_cache = {}
        self._list_cache = {}
        self._unrank_cache = {}
        self._rank_cache = {}

    @abstractmethod
    def calc_valuation(self):
        pass

    @abstractmethod
    def _count(self, i):
        pass

    @abstractmethod
    def _bound_count(self, min, max):
        pass

    @abstractmethod
    def _list(self, n):
        pass

    @abstractmethod
    def _unrank(self, n, k):
        pass

    @abstractmethod
    def _rank(self, obj):
        pass

    @functools.lru_cache(maxsize=None)
    def count(self, i):
        return self._count(i)

    @functools.lru_cache(maxsize=None)
    def bound_count(self, min, max):
        return self._bound_count(min, max)

    @functools.lru_cache(maxsize=None)
    def list(self, n):
        return self._list(n)

    @functools.lru_cache(maxsize=None)
    def unrank(self, n, k):
        return self._unrank(n, k)

    @functools.lru_cache(maxsize=None)
    def rank(self, obj):
        return self._rank(obj)

    def random(self, n):
        return self.unrank(n, random.randint(0, self.count(n) - 1))

    def set_grammar(self, grammar):
        self._grammar = grammar


class ConstructorRule(AbstractRule):
    def __init__(self, fst, snd, dec):
        super(ConstructorRule, self).__init__()
        assert type(fst) == str
        assert type(snd) == str
        assert callable(dec)
        self._fst = fst
        self._snd = snd
        self._dec = dec


class ConstantRule(AbstractRule):
    def __init__(self, obj):
        super(ConstantRule, self).__init__()
        self._object = obj

    def _rank(self, obj):
        if obj != self._object:
            raise ValueError("Invalid object")
        return 0


class SingletonRule(ConstantRule):
    def __init__(self, obj):
        super(SingletonRule, self).__init__(obj)

    def __str__(self):
        return 'Singleton("{}")'.format(self._object)

    def __repr__(self):
        return str(self)

    def calc_valuation(self):
        return 1

    def _count(self, i):
        return 1 if i == 1 else 0

    def _bound_count(self, min, max):
        return 1 if min <= 1 and 1 < max else 0

    def _list(self, n):
        return [self._object] if n == 1 else []

    def _unrank(self, n, k):
        if k >= self.count(n):
            raise ValueError("Rank greater than count!")
        return self._object


class EpsilonRule(ConstantRule):
    def __init__(self, obj):
        super(EpsilonRule, self).__init__(obj)

    def __str__(self):
        return 'Epsilon("{}")'.format(self._object)

    def __repr__(self):
        return str(self)

    def calc_valuation(self):
        return 0

    def _count(self, i):
        return 1 if i == 0 else 0

    def _bound_count(self, min, max):
        return 1 if min <= 0 and 0 < max else 0

    def _list(self, n):
        return [self._object] if n == 0 else []

    def _unrank(self, n, k):
        if k >= self.count(n):
            raise ValueError("Rank greater than count!")
        return self._object


class UnionRule(ConstructorRule):
    def __init__(self, fst, snd, dec=lambda: True):
        super(UnionRule, self).__init__(fst, snd, dec)

    def __str__(self):
        return 'UnionRule("{}","{}")'.format(self._fst, self._snd)

    def __repr__(self):
        return str(self)

    def calc_valuation(self):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        return val_fst if val_fst < val_snd else val_snd

    def _count(self, i):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        count_fst = 0 if i < val_fst else self._grammar[self._fst].count(i)
        count_snd = 0 if i < val_snd else self._grammar[self._snd].count(i)
        return count_fst + count_snd

    def _bound_count(self, min, max):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        count_fst = 0 if max < val_fst else self._grammar[self._fst].bound_count(min, max)
        count_snd = 0 if max < val_snd else self._grammar[self._snd].bound_count(min, max)
        return count_fst + count_snd

    def _list(self, n):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        list_fst = [] if n < val_fst else self._grammar[self._fst].list(n)
        list_snd = [] if n < val_snd else self._grammar[self._snd].list(n)
        return list_fst + list_snd

    def _unrank(self, n, k):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        count_fst = 0 if n < val_fst else self._grammar[self._fst].count(n)
        count_snd = 0 if n < val_snd else self._grammar[self._snd].count(n)
        if k >= count_fst + count_snd:
            raise ValueError("Rank greater than count!")
        if k < count_fst:
            return self._grammar[self._fst].unrank(n, k)
        else:
            return self._grammar[self._snd].unrank(n, k - count_fst)

    def _rank(self, obj):
        count = 0 if self._dec(obj) else self._grammar[self._fst].count(len(obj))
        rank = count + self._grammar[self._fst if self._dec(obj) else self._snd].rank(
            obj,
        )
        return rank


class ProductRule(ConstructorRule):
    def __init__(self, fst, snd, cons, dec=lambda x: (True, x)):
        super(ProductRule, self).__init__(fst, snd, dec)
        assert callable(cons)
        self._cons = cons

    def __str__(self):
        return 'ProductRule("{}","{}")'.format(self._fst, self._snd)

    def __repr__(self):
        return str(self)

    def calc_valuation(self):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        return val_fst + val_snd

    def _count(self, i):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        count_total = 0
        for k in range(i + 1):
            l = i - k
            if k >= val_fst and l >= val_snd:
                count_fst = self._grammar[self._fst].count(k)
                count_snd = self._grammar[self._snd].count(l)
                count_total += count_fst * count_snd
        return count_total

    def _bound_count(self, min, max):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        count_total = 0
        counts_fst = {}
        counts_snd = {}
        for i in range(0, max):
            if i >= val_fst:
                counts_fst[i] = self._grammar[self._fst].count(i)
            if i >= val_snd:
                counts_snd[i] = self._grammar[self._snd].count(i)
        for i in range(val_fst, max):
            for j in range(val_snd, max):
                if i + j >= min and i + j < max:
                    count_total += counts_fst[i] * counts_snd[j]
        return count_total

    def _list(self, n):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        list_total = []
        for k in range(n + 1):
            l = n - k
            if k >= val_fst and l >= val_snd:
                list_fst = self._grammar[self._fst].list(k)
                list_snd = self._grammar[self._snd].list(l)
                for obj_fst in list_fst:
                    for obj_snd in list_snd:
                        list_total += [self._cons([obj_fst, obj_snd])]
        return list_total

    def _unrank(self, n, m):
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        for k in range(n + 1):
            l = n - k
            if k >= val_fst and l >= val_snd:
                count_fst = self._grammar[self._fst].count(k)
                count_snd = self._grammar[self._snd].count(l)
                if m < count_snd * count_fst:
                    obj_fst = self._grammar[self._fst].unrank(k, m // count_snd)
                    obj_snd = self._grammar[self._snd].unrank(l, m % count_snd)
                    return self._cons([obj_fst, obj_snd])
                else:
                    m -= count_snd * count_fst
        raise ValueError("Rank greater than count!")

    def _rank(self, obj):
        obj_fst, obj_snd = self._dec(obj)
        val_fst = self._grammar[self._fst].valuation
        val_snd = self._grammar[self._snd].valuation
        rank = 0
        for k in range(len(obj_fst)):
            l = len(obj) - k
            if k >= val_fst and l >= val_snd:
                count_fst = self._grammar[self._fst].count(k)
                count_snd = self._grammar[self._snd].count(l)
                rank += count_fst * count_snd
        rank_fst = self._grammar[self._fst].rank(obj_fst,)
        rank_snd = self._grammar[self._snd].rank(obj_snd,)
        count_snd = self._grammar[self._snd].count(len(obj_snd))
        rank += rank_fst * count_snd + rank_snd
        return rank


def check_grammar(grammar):
    non_terminals = grammar.keys()
    for name, rule in grammar.items():
        if isinstance(rule, ConstructorRule):
            for nt in [rule._fst, rule._snd]:
                if nt not in non_terminals:
                    print('"{}" not found in grammar!'.format(nt))
                    return False
    return True


def check_ambiguity(grammar, root, n_max=6):
    for n in range(n_max):
        L = grammar[root].list(n)
        if len(L) != len(set(L)):
            return True
    return False


def init_grammar(grammar):
    assert check_grammar(grammar)
    for rule in grammar.values():
        rule.set_grammar(grammar)
    continue_iteration = True
    max_iterations = 100
    while continue_iteration and max_iterations > 0:
        continue_iteration = False
        max_iterations -= 1
        for rule in grammar.values():
            new_valuation = rule.calc_valuation()
            if rule.valuation != new_valuation:
                continue_iteration = True
                rule.valuation = new_valuation
