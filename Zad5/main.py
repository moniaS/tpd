import heapq
import cmd
import sys

class Process:
    def __init__(self, name, time):
        self.name = name
        self.time = time
    
    def get_time(self):
        return self.time

    def get_name(self):
        return self.name

    def __lt__(self, other):
        return self.time < other.time

class Machine:
    def __init__(self, id):
        self.id = id
        self.process_list = []
        self.total_processing_time = 0

    def get_processList(self):
        return self.processList

    def add_process(self, process):
        self.processList.append(process)
        self.total_processing_time = total_processing_time + process.get_time()

    def get_total_processing_time(self):
        return self.total_processing_time

    def __lt__(self, other):
        return self.total_processing_time < other.total_processing_time

list_of_all_processes = []
number_of_processors = input("Podaj liczbę procesorów: ")

file = open("data.txt", "r")
for line in file:
    line2 = line.split()
    process = Process(line2[0], line2[1])
    list_of_all_processes.append(process)

for process in list_of_all_processes:
    print("Nazwa: " + process.get_name() + ", czas wykonywania: " + process.get_time())

list_of_processors = []
for i in range(1, int(number_of_processors)+1):
    machine = Machine(i)
    list_of_processors.append(machine)

#tworzymy kolejke priorytetowa z rosnącymi czasami wykonywania procesów
processes_queue = [(p.get_time(), p) for p in list_of_all_processes]
heapq.heapify(processes_queue)

#tworzymy kolejke priorytetowa maszyn wedlug całkowitego czasu procesow na maszynie
machine_queue = [(p.get_total_processing_time(), p) for p in list_of_processors]
heapq.heapify(machine_queue)

while len(processes_queue):
    p = heapq.heappop(processes_queue)
    print(p[1].get_time())