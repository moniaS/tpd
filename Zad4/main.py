import sys
import heapq
import numpy as numpy

class Vertex:
    def __init__(self, node):
        self.id = node
        self.next = {}
        self.previous = {}
        self.distance = 0

    def add_next(self, neighbour, weight):
        self.next[neighbour] = weight
    
    def get_next(self):
        return self.next.keys()  

    def add_previous(self, prev):
        self.previous = prev

    def get_previous(self):
        return self.previous.keys()  

    def get_id(self):
        return self.id

    #def get_weight(self, neighbor):
    #    return self.next[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance



    #def __str__(self):
    #    return 'wierzchołek: ' + str(self.id) + ' sąsiedzi: ' + str([x.id for x in self.adjacent])

    #def __lt__(self, other):
    #    return self.distance < other.distance

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_next(self.vert_dict[to], cost)
        self.vert_dict[to].add_previous(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

matrix = numpy.loadtxt('matrix.txt')
print("Wczytana macierz:")
print(matrix)

graph = Graph()

for i, row in enumerate(matrix):
    if i not in graph.get_vertices():
        graph.add_vertex(i)
        print("dodaje wierzcholek %d" % i)
    for j in range(0, matrix.shape[1]):
        if i == 0 and j != 0:
            graph.add_vertex(j)
            print("dodaje wierzcholek %d" % j)
        if matrix[i][j] >= 0:
            graph.add_edge(i, j, matrix[i][j])

#print ('\nKrawędzie grafu:')
vertexLastStage = []
for v in graph:
    for w in v.get_connections():
        #sprawdzamy czy istnieje wierzchołek o wiekszym id, jesli nie to znaczy ze jest to wierzcholek z ostatniego etapu
        if w.get_id() > v.get_id():
            vertexLastStage.append(v)
        #print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
