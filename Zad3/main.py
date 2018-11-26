import sys
import heapq
import numpy as numpy

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.distance = sys.maxsize
        self.visited = False  
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return 'wierzchołek: ' + str(self.id) + ' sąsiedzi: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other):
        return self.distance < other.distance

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

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortestPath(v, path):
    if v.previous:
        path.append(v.previous.get_id())
        shortestPath(v.previous, path)
    return

#złożoność to chyba O(E\log V) gdzie E - liczba krawędzi grafu a V liczba wierzchołkow, ale nie jestem pewna
def dijkstra(aGraph, start):
    print ('\n------- ALGORYTM DIJKSTRA --------\n')

    #wierzcholkowi od ktorego startujemy przypisujemy wartosc 0
    start.set_distance(0)

    #tworzymy tuple z parami dystans-wierzchołek z pozostalych wierzcholkow (pozostale wierzcholki w pierwszej iteracji maja przypisana duza odleglosc)
    #v in aGraph to iteracja po wszystkich krawędziach grafu - taki zapis możliwy dzięki definicji funkcji __iter__ w klasie Graph
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]

    # wrzucamy ją do kolejki priorytetowej
    heapq.heapify(unvisited_queue)

    #dopóki kolejka nie jest pusta
    while len(unvisited_queue):
        # pobieramy pierwszy element w kolejce - wierzchołek najbliższy źródła który nie został jeszcze rozważony
        uv = heapq.heappop(unvisited_queue)
        #wyciągamy obiekt wierzchołka z tupli
        current = uv[1]
        current.set_visited()

        #iterujemy sąsiadów danego wierzchołka
        for next in current.adjacent:
            #nie interesują nas odwiedzone wierzchołki
            if next.visited:
                continue

            #obliczamy nowa odleglosc (suma odleglosci do biezacego wierzcholka plus odleglosc do nowego wierzcholka)
            new_dist = current.get_distance() + current.get_weight(next)
            
            #relaksacja - zmiana odległości minimalnej ścieżki jeśli nowa obliczona ścieżka jest krótsza od poprzednio wyliczonej dla danego wierzchołka
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                print ('Znaleziono nowe połączenie w drzewie : bieżący wierzchołek = %s, kolejny wierzchołek = %s, nowa odległość = %s' \
                        %(current.get_id(), next.get_id(), next.get_distance()))
            else:
                print ('Nie połączono: bieżący wierzchołek = %s następny wierzchołek = %s nowa odległość = %s' \
                        %(current.get_id(), next.get_id(), next.get_distance()))

        # tworząc i sortując ponownie kolejkę upewniamy się że następny pobrany element ma już nadaną wagę - jest sąsiedem innego odwiedzonego wierzchołka
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

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

print ('\nKrawędzie grafu:')
for v in graph:
    for w in v.get_connections():
        vid = v.get_id()
        wid = w.get_id()
        print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))

#od ktorego punktu chcemy liczyc odleglosci?
source = 1

dijkstra(graph, graph.get_vertex(source)) 

for i in range(0, matrix.shape[1]):
    if i == source:
        continue
    target = graph.get_vertex(i)
    path = [i]
    shortestPath(target, path)
    #wyswietlamy odwrocona droge od 0 do danego wierzchołka
    print ('Najkrótsza droga od wierzchołka %d do %d : %s, odlogosc: %d' %(source, i, path[::-1], target.get_distance()))