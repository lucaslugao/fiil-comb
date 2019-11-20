
# Report UE5
## Authors
Lucas LUGÃO GUIMARÃES
Victor Hugo VIANNA SILVA
## Grammar counts (Q1)
### Tree

|n|Tree|Node|Leaf|
|-|-|-|-|
|0|0|0|0|
|1|1|0|1|
|2|1|1|0|
|3|2|2|0|
|4|5|5|0|
|5|14|14|0|
|6|42|42|0|
|7|132|132|0|
|8|429|429|0|
|9|1430|1430|0|
|10|4862|4862|0|

### Fibonacci

|n|Fib|Cas1|Cas2|Vide|CasAu|AtomA|AtomB|CasBAu|
|-|-|-|-|-|-|-|-|-|
|0|1|0|0|1|0|0|0|0|
|1|2|2|1|0|1|1|1|0|
|2|3|3|1|0|2|0|0|1|
|3|5|5|2|0|3|0|0|2|
|4|8|8|3|0|5|0|0|3|
|5|13|13|5|0|8|0|0|5|
|6|21|21|8|0|13|0|0|8|
|7|34|34|13|0|21|0|0|13|
|8|55|55|21|0|34|0|0|21|
|9|89|89|34|0|55|0|0|34|
|10|144|144|55|0|89|0|0|55|

## Grammar definitions (Q2-Q6)
```python
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
```
## Check all non-terminals are defined (Q7)
```python
def check_grammar(grammar):
    non_terminals = grammar.keys()
    for name, rule in grammar.items():
        if isinstance(rule, ConstructorRule):
            for nt in [rule._fst, rule._snd]:
                if nt not in non_terminals:
                    print('"{}" not found in grammar!'.format(nt))
                    return False
    return True
```
## Valuations (Q8)

### treeGram

n|Tree|Node|Leaf
-|-|-|-
0|$\infty$|$\infty$|$\infty$
1|$\infty$|$\infty$|1
2|1|$\infty$|1
3|1|2|1
4|1|2|1
final|1|2|1


### fiboGram

n|Fib|Cas1|Cas2|Vide|CasAu|AtomA|AtomB|CasBAu
-|-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|$\infty$|$\infty$|$\infty$|0|$\infty$|1|1|$\infty$
2|0|$\infty$|1|0|$\infty$|1|1|$\infty$
3|0|1|1|0|1|1|1|$\infty$
4|0|1|1|0|1|1|1|2
5|0|1|1|0|1|1|1|2
final|0|1|1|0|1|1|1|2


### abGram

n|E|A|B|W|AW|BW|AW\|BW
-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$
2|0|1|1|0|$\infty$|$\infty$|$\infty$
3|0|1|1|0|1|1|$\infty$
4|0|1|1|0|1|1|1
5|0|1|1|0|1|1|1
final|0|1|1|0|1|1|1


### dyckGram

n|E|(|)|W|(W)W|(W)|(W
-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$
2|0|1|1|0|$\infty$|$\infty$|$\infty$
3|0|1|1|0|$\infty$|$\infty$|1
4|0|1|1|0|$\infty$|2|1
5|0|1|1|0|2|2|1
6|0|1|1|0|2|2|1
final|0|1|1|0|2|2|1


### max3Gram

n|E|A|B|W|A1|B1|A2|B2|E\|A2\|B1|E\|B2\|A1|A2\|B1|B2\|A1|A1\|B1|E\|B1|E\|A1
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
2|0|1|1|0|$\infty$|$\infty$|$\infty$|$\infty$|0|0|$\infty$|$\infty$|$\infty$|0|0
3|0|1|1|0|1|1|1|1|0|0|$\infty$|$\infty$|$\infty$|0|0
4|0|1|1|0|1|1|1|1|0|0|1|1|1|0|0
5|0|1|1|0|1|1|1|1|0|0|1|1|1|0|0
final|0|1|1|0|1|1|1|1|0|0|1|1|1|0|0


### abPalindromeGram

n|E|A|B|W|A\|B\|AWA\|BWB|B\|AWA\|BWB|AWA\|BWB|AW|AWA|BW|BWB
-|-|-|-|-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
2|0|1|1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
3|0|1|1|0|1|1|$\infty$|1|$\infty$|1|$\infty$
4|0|1|1|0|1|1|$\infty$|1|2|1|2
5|0|1|1|0|1|1|2|1|2|1|2
6|0|1|1|0|1|1|2|1|2|1|2
final|0|1|1|0|1|1|2|1|2|1|2


### abcPalindromeGram

n|E|A|B|C|W|A\|B\|C\|AWA\|BWB\|CWC|B\|C\|AWA\|BWB\|CWC|C\|AWA\|BWB\|CWC|AWA\|BWB\|CWC|BWB\|CWC|AW|AWA|BW|BWB|CW|CWC
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|0|1|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
2|0|1|1|1|0|1|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
3|0|1|1|1|0|1|1|1|$\infty$|$\infty$|1|$\infty$|1|$\infty$|1|$\infty$
4|0|1|1|1|0|1|1|1|$\infty$|$\infty$|1|2|1|2|1|2
5|0|1|1|1|0|1|1|1|2|2|1|2|1|2|1|2
6|0|1|1|1|0|1|1|1|2|2|1|2|1|2|1|2
final|0|1|1|1|0|1|1|1|2|2|1|2|1|2|1|2


### abEqualCountGram

n|E|A|B|W|a|b|AbW\|BaW|AbW|Abb|Baa|BaW|bW|aW|aa|bb
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
0|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
2|0|1|1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
3|0|1|1|0|1|1|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|1|1|2|2
4|0|1|1|0|1|1|$\infty$|2|3|3|2|1|1|2|2
5|0|1|1|0|1|1|2|2|3|3|2|1|1|2|2
6|0|1|1|0|1|1|2|2|3|3|2|1|1|2|2
final|0|1|1|0|1|1|2|2|3|3|2|1|1|2|2

## Smallest objects (Q9)

### treeGram

NT|Min object|Valuation
--|--|--
Tree|"Leaf"|1
Node|"Node(Leaf,Leaf)"|2
Leaf|"Leaf"|1

### fiboGram

NT|Min object|Valuation
--|--|--
Fib|""|0
Cas1|"A"|1
Cas2|"B"|1
Vide|""|0
CasAu|"A"|1
AtomA|"A"|1
AtomB|"B"|1
CasBAu|"BA"|2

### abGram

NT|Min object|Valuation
--|--|--
E|""|0
A|"A"|1
B|"B"|1
W|""|0
AW|"A"|1
BW|"B"|1
AW\|BW|"A"|1

### dyckGram

NT|Min object|Valuation
--|--|--
E|""|0
(|"("|1
)|")"|1
W|""|0
(W)W|"()"|2
(W)|"()"|2
(W|"("|1

### max3Gram

NT|Min object|Valuation
--|--|--
E|""|0
A|"A"|1
B|"B"|1
W|""|0
A1|"A"|1
B1|"B"|1
A2|"A"|1
B2|"B"|1
E\|A2\|B1|""|0
E\|B2\|A1|""|0
A2\|B1|"A"|1
B2\|A1|"B"|1
A1\|B1|"A"|1
E\|B1|""|0
E\|A1|""|0

### abPalindromeGram

NT|Min object|Valuation
--|--|--
E|""|0
A|"A"|1
B|"B"|1
W|""|0
A\|B\|AWA\|BWB|"A"|1
B\|AWA\|BWB|"B"|1
AWA\|BWB|"AA"|2
AW|"A"|1
AWA|"AA"|2
BW|"B"|1
BWB|"BB"|2

### abcPalindromeGram

NT|Min object|Valuation
--|--|--
E|""|0
A|"A"|1
B|"B"|1
C|"C"|1
W|""|0
A\|B\|C\|AWA\|BWB\|CWC|"A"|1
B\|C\|AWA\|BWB\|CWC|"B"|1
C\|AWA\|BWB\|CWC|"C"|1
AWA\|BWB\|CWC|"AA"|2
BWB\|CWC|"BB"|2
AW|"A"|1
AWA|"AA"|2
BW|"B"|1
BWB|"BB"|2
CW|"C"|1
CWC|"CC"|2

### abEqualCountGram

NT|Min object|Valuation
--|--|--
E|""|0
A|"A"|1
B|"B"|1
W|""|0
a|"A"|1
b|"B"|1
AbW\|BaW|"AB"|2
AbW|"AB"|2
Abb|"ABB"|3
Baa|"BAA"|3
BaW|"BA"|2
bW|"B"|1
aW|"A"|1
aa|"AA"|2
bb|"BB"|2

## Consistency tests (Q13)

- rule.list(n) == [rule.unrank(n, i) for i in range(0, rule.count(n))]

- every element in rule.list(n) must have size n

- all([rule.rank(obj) == i for i, obj in enumerate(rule.list(n))])
