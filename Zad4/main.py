import sys
import heapq
import numpy as numpy

class Vertex:
    def __init__(self, node):
        self.id = node
        self.nextStage = {}
        self.previousStage = {}
        self.bestDistanceTillEnd = sys.maxsize
        self.bestNext = None

    def add_nextStage(self, neighbour, weight):
        self.nextStage[neighbour] = weight
    
    def get_nextStage(self):
        return self.nextStage.keys()  

    def add_previousStage(self, prev, weight):
        self.previousStage[prev] = weight

    def get_previousStage(self):
        return self.previousStage.keys()  

    def get_id(self):
        return self.id

    def get_weightNext(self, neighbor):
        return self.nextStage[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance
    
    def set_bestNext(self, next):
        self.bestNext = next
    
    def get_bestNext(self):
        return self.bestNext

    def get_bestDistanceTillEnd(self):
        return self.bestDistanceTillEnd

    def set_bestDistanceTillEnd(self, best):
        self.bestDistanceTillEnd = best

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

        self.vert_dict[frm].add_nextStage(self.vert_dict[to], cost)
        self.vert_dict[to].add_previousStage(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def getVerticesFromPreviousStage(currentStage):
    vertexPreviousStage = []
    for v in currentStage:
        for w in v.get_previousStage():
            if not vertexPreviousStage.__contains__(w):
                vertexPreviousStage.append(w)
    return vertexPreviousStage

def mapMatrixToGraph(matrix):
    graph = Graph()
    for i, row in enumerate(matrix):
        if i not in graph.get_vertices():
            graph.add_vertex(i)
            print("dodaje wierzcholek %d" % (int(i) + 1))
        for j in range(0, matrix.shape[1]):
            if i == 0 and j != 0:
                graph.add_vertex(j)
                print("dodaje wierzcholek %d" % (int(j) + 1))
            if matrix[i][j] >= 0:
                graph.add_edge(i, j, matrix[i][j])
    return graph

def getVerticesFromLastStage(graph):
    vertexLastStage = []
    for v in graph:
        if not v.get_nextStage():
            #dla wierzcholkow na ostatnim etapie ustawiamy ich odleglosc od erapu koncowego na 0
            v.set_bestDistanceTillEnd(0)
            vertexLastStage.append(v)
    return vertexLastStage

#zwraca wierzchołki z pierwszego etapu zeby mozna bylo wybrac ten z droga najbardziej optymalna
def algorithm(verticesCurrentStage):
    vertexPreviousStage = getVerticesFromPreviousStage(verticesLastStage)
    
    #dopoki nie dotarlismy do pierwszego etapu
    while bool(vertexPreviousStage):
        vertexCurrentStage = vertexPreviousStage
        #dla kazdego wiercholka z poprzedniego etapu musimy ustalic minimalna droge do koncowego etapu
        for v in vertexPreviousStage:
            verticesFromNextStage = v.get_nextStage()
            for w in verticesFromNextStage:
                #jesli znaleziona droga do konca jest krotsza od tej aktualnie zapisanej to zamien 
                if (v.get_weightNext(w) + w.get_bestDistanceTillEnd()) < v.get_bestDistanceTillEnd():
                    v.set_bestDistanceTillEnd(v.get_weightNext(w) + w.get_bestDistanceTillEnd())
                    v.set_bestNext(w)
                    print("Dla wierzcholka %d ustawiamy dystans %d i kolejny wierzcholek %d" % (int(v.get_id()) + 1, v.get_bestDistanceTillEnd(), int(v.get_bestNext().get_id()) + 1))
        vertexPreviousStage = getVerticesFromPreviousStage(vertexPreviousStage)
    return vertexCurrentStage

def findOptimalStrategy(verticesFirstStage):
    bestVerticeToBegin = verticesFirstStage[0]
    for v in verticesFirstStage:
        if v.get_bestDistanceTillEnd() < bestVerticeToBegin.get_bestDistanceTillEnd():
            bestVerticeToBegin = v
    print("\nRozwiązanie optymalne: %d" % bestVerticeToBegin.get_bestDistanceTillEnd())

    strategy = "Strategia optymalna: "
    strategy += str(int(bestVerticeToBegin.get_id()) + 1)
    currentVertice = bestVerticeToBegin
    while bool(currentVertice.get_bestNext()):
        currentVertice = currentVertice.get_bestNext()
        strategy += " -> "
        strategy += str(int(currentVertice.get_id()) + 1)
    print(strategy)


matrix = numpy.loadtxt('matrix.txt')
print("Wczytana macierz:")
print(matrix)

graph = mapMatrixToGraph(matrix)

verticesLastStage = getVerticesFromLastStage(graph)
verticesFirstStage = algorithm(verticesLastStage)
for v in graph:
    print("Wierzchołek %d ma optymalną odległość do końca: %d" % (int(v.get_id()) + 1, v.get_bestDistanceTillEnd()))

print("-------- WYBOR STRATEGII OPTYMALNEJ I ROZWIĄZANIA OPTYMALNEGO ---------")

findOptimalStrategy(verticesFirstStage)