import heapq
import random

class Process:
    def __init__(self, id, time):
        self.id = id
        self.time = int(time)
    
    def get_time(self):
        return self.time

    def get_id(self):
        return self.id

    def __lt__(self, other):
        return self.time < other.time

class Machine:
    def __init__(self, id):
        self.id = id
        self.process_list = []
        self.total_processing_time = 0

    def get_processList(self):
        return self.process_list

    def add_process(self, process):
        self.process_list.append(process)
        self.total_processing_time = self.total_processing_time + process.get_time()

    def get_total_processing_time(self):
        return self.total_processing_time

    def __lt__(self, other):
        return self.total_processing_time < other.total_processing_time

    def __str__(self):
        return 'Procesor ' + str(self.id) + ', czas trwania procesów :' + str([p.time for p in self.process_list]) + ', całkowity czas wykonywania: ' + str(self.total_processing_time)

def read_processes():
    list_of_all_processes = []
    #file = open("data.txt", "r")
    #for line in file:
    #    line2 = line.split()
    #    process = Process(line2[0], line2[1])
    #    list_of_all_processes.append(process)
    number_of_processes = input("Podaj liczbę zadań: ")
    for i in range(1, int(number_of_processes) + 1):
        list_of_all_processes.append(Process(i, random.randint(1,101)))

    print("\nWczytane procesy:")
    for process in list_of_all_processes:
        print("Id zadania: " + str(process.get_id()) + ", czas wykonywania: " + str(process.get_time()))
    return list_of_all_processes

def create_processors():
    number_of_processors = input("\nPodaj liczbę procesorów: ")
    list_of_processors = []
    for i in range(1, int(number_of_processors) + 1):
        machine = Machine(i)
        list_of_processors.append(machine)
    return list_of_processors


list_of_all_processes = read_processes()
list_of_processors = create_processors()

#tworzymy kolejke priorytetowa z rosnącymi czasami wykonywania procesów
processes_queue = [(p.get_time(), p) for p in list_of_all_processes]
heapq.heapify(processes_queue)

#tworzymy kolejke priorytetowa maszyn wedlug całkowitego czasu procesow na maszynie
machine_queue = [(p.get_total_processing_time(), p) for p in list_of_processors]
heapq.heapify(machine_queue)

while len(processes_queue):
    process = heapq.heappop(processes_queue)
    machine = heapq.heappop(machine_queue)
    machine[1].add_process(process[1])
    machine_queue.append(machine)

print("\nPrzydział zadań:")
for m in list_of_processors:
    print(m)