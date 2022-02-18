import random


class Vertex:
    def __init__(self, value):
        self.value = value
        self.adjacent = {}
        self.adjacentL = []
        self.adjW = []

    def add_edge(self, adj, weight=0):
        self.adjacent[adj] = weight

    def add_weight(self, adj):
        self.adjacent[adj] = self.adjacent.get(adj, 0) + 1

    def get_Map(self):
        for (vertex, weight) in self.adjacent.items():
            self.adjacentL.append(vertex)
            self.adjW.append(weight)

    def get_Next(self):
        return random.choices(self.adjacentL, weights=self.adjW)[0]


class Graph:
    def __init__(self):
        self.Vlist = {}

    def add_vertex(self, value):
        self.Vlist[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.Vlist:
            self.add_vertex(value)
        return self.Vlist[value]

    def Next(self, vertex):
        return self.Vlist[self.Vlist[vertex.value].get_Next()]

    def Generate_PMaps(self):
        for vertex in self.Vlist.values():
            vertex.get_Map()
