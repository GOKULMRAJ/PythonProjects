import random
import string
from Graph import Vertex, Graph


def get_Words(path):
    with open(path, 'r') as F:
        Text = F.read()
    Text = ' '.join(Text.split())
    Text = Text.lower()
    Text = Text.translate(str.maketrans('', '', string.punctuation))

    words = Text.split()
    return words


def Form_Graph(words):
    G = Graph()
    flag = None
    for word in words:
        vertex = G.get_vertex(word)
        if flag:
            flag.add_weight(word)
        flag = vertex
    G.Generate_PMaps()
    return G


def compose(G, words, length):
    Composition = []
    word = G.get_vertex(random.choice(words))
    for _ in range(length):
        Composition.append(word.value)
        word = G.Next(word)
    return Composition


def main():
    words = get_Words('Texts/Sorcerer_Stone.txt')
    G = Form_Graph(words)
    Final = compose(G, words, 5)
    return ' '.join(Final)


if __name__ == '__main__':
    print(main())
