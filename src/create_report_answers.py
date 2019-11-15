from rules import *
import grammars
from importlib import reload


def init_grammar_verbose(grammar):
    for rule in grammar.values():
        rule.set_grammar(grammar)

    valuation_algo_output = ""

    def add_to_output(*v):
        nonlocal valuation_algo_output
        valuation_algo_output += "|".join([str(x).replace("|", "\|") for x in v]) + "\n"

    add_to_output("n", *grammar.keys())
    add_to_output("-", *["-" for _ in grammar.keys()])
    valuations = {rule_name: rule.valuation for rule_name, rule in grammar.items()}

    def print_valuations(n):
        nonlocal grammar, add_to_output
        add_to_output(
            n,
            *[
                str(rule.valuation) if rule.valuation < float("inf") else "$\infty$"
                for rule in grammar.values()
            ]
        )

    n = 0
    print_valuations(n)

    continue_iteration = True
    while continue_iteration:
        new_valuations = {
            rule_name: rule.calc_valuation() for rule_name, rule in grammar.items()
        }
        continue_iteration = False
        for rule_name, new_valuation in new_valuations.items():
            if grammar[rule_name].valuation != new_valuation:
                continue_iteration = True
            grammar[rule_name].valuation = new_valuation
        n += 1
        print_valuations(n)

    print_valuations("final")
    return valuation_algo_output


def q1():
    print("## 1.")
    reload(grammars)

    def print_counts(grammar):
        print("", "n", *grammar.keys(), "", sep="|")
        print("", *["-"] * (1 + len(grammar)), "", sep="|")
        for n in range(0, 11):
            print("", n, *[rule.count(n) for rule in grammar.values()], "", sep="|")

    init_grammar(grammars.grammars["treeGram"])
    init_grammar(grammars.grammars["fiboGram"])
    print("# Tree Grammar counts\n")
    print_counts(grammars.grammars["treeGram"])
    print("\n# Fibonacci Grammar counts\n")
    print_counts(grammars.grammars["fiboGram"])


def q8():
    print("## 8.")
    reload(grammars)
    for grammar_name, grammar in grammars.grammars.items():
        algo_out = init_grammar_verbose(grammar)
        print("\n# {}\n".format(grammar_name))
        print(algo_out)


def q9():
    print("## 9.")
    reload(grammars)
    for grammar_name, grammar in grammars.grammars.items():
        init_grammar(grammar)
        print("\n**{}**\n".format(grammar_name))
        print("|".join(["NT", "Min object", "Valuation"]))
        print("|".join(["--"] * 3))
        for rule_name, rule in grammar.items():
            print(
                "|".join(
                    [
                        rule_name.replace("|", "\|"),
                        '"{}"'.format(rule.unrank(rule.valuation, 0)),
                        str(rule.valuation),
                    ]
                )
            )



def print_grammar(grammar):
    for rule_name, rule in grammar.items():
        print(rule_name, str(rule))


if __name__ == "__main__":
    q1()
    q8()
    q9()