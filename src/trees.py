class Node:
    def __init__(self, fst, snd):
        self._fst = fst
        self._snd = snd

    def __str__(self):
        return "Node({},{})".format(self._fst, self._snd)

    def __eq__(self, other):
        return self._fst == other._fst and self._snd == other._snd

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self._fst) + len(self._snd)


class Leaf:
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Leaf)

    def __str__(self):
        return "Leaf"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return 1
