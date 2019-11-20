class Node:
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd

    def __str__(self):
        return "Node({},{})".format(self.fst, self.snd)

    def __eq__(self, other):
        return self.fst == other.fst and self.snd == other.snd

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.fst) + len(self.snd)


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
