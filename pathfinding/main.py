import csv
import os
from queue import PriorityQueue
from io import open

# file path. << really?
FILE_PATH = "./pathfinding/cities.csv"

cities = {}


def PrintCities(cities):
    print("Search Space Graph")
    print("--------------------------------------------------------------------------")
    for city in cities:
        print(city, cities[city].neighbors)
    print("--------------------------------------------------------------------------")


class CityNotFoundError(Exception):
    def __init__(self, city):
        print(f"{city} not found")
        pass


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}


def build_graph(path, printMap):
    with open(FILE_PATH, "r", encoding="UTF-8") as file:
        reader = csv.reader(file)
        next(reader)

        for line in reader:
            print(line)
            city1 = line[0].lower()
            city2 = line[1].lower()
            weight = line[2]

            # Add cities to the dictionary if they don't already exist
            if city1 not in cities:
                cities[city1] = Node(city1)
            if city2 not in cities:
                cities[city2] = Node(city2)

            # Add the weight(distance) of each edge between the cities.
            cities[city1].neighbors[city2] = int(weight)
            cities[city2].neighbors[city1] = int(weight)

    if printMap:
        PrintCities(cities)


def check_cities(start, end):
    if start not in cities:
        raise CityNotFoundError(start)
    if end not in cities:
        raise CityNotFoundError(end)


def uniform_cost_search(
    cities, start, end
):  # < idk why cities are passed here, despite being constant, but okay
    check_cities(start, end)

    visited = set()
    queue = PriorityQueue()
    queue.put((0, start, [start]))
    print(f"initializing priority queues : {list(queue.queue)}", " \n")

    while queue:
        print(f"dequeueing...")
        cost, current, route = queue.get()

        if current not in visited:
            visited.add(current)

            if current == end:
                print("goal state found!")
                print("From " + start + " to " + end + ", your shortest route is: ")
                print(" -> ".join(route))
                print("With cost of", cost, "unit distance.\n")
                return

            neighbors = cities[current].neighbors
            for city in neighbors:
                if city not in visited:
                    total_cost = cost + neighbors[city]
                    print(
                        f"checking {current}({neighbors}) -> {city}, total cost: {total_cost}"
                    )
                    queue.put(
                        (total_cost, cities[city].name, route + [cities[city].name])
                    )
                    print(f"enqueueing {city} :", list(queue.queue), "\n")


def breadth_first_search(cities, start, end):
    check_cities(start, end)

    visited = set()
    queue = []
    path = {}

    queue.append(start)

    while queue:
        current = queue.pop(0)

        if current not in visited:
            visited.add(current)

            if current == end:
                print("goal state found")
                route = [end]
                while route[-1] != start:
                    route.append(path[route[-1]])
                route.reverse()
                print("From " + start + " to " + end + ", your path is: ")
                print(" -> ".join(route))
            neighbors = cities[current].neighbors
            for city in neighbors:
                if city not in visited:
                    queue.append(city)
                    path[city] = current


def depth_first_search(cities, start, end):
    check_cities(start, end)

    visited = set()
    stack = []
    path = {}

    stack.append(start)

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.add(current)

            if current == end:
                print("goal state found")
                route = [end]
                while route[-1] != start:
                    route.append(path[route[-1]])
                route.reverse()
                print("From " + start + " to " + end + ", your path is: ")
                print(" -> ".join(route))
            neighbors = cities[current].neighbors
            for city in neighbors:
                if city not in visited:
                    stack.append(city)
                    path[city] = current


def inputExit(var):
    if var == "exit":
        print("Exiting...")
        return True
    return False


PRINT_GRAPH = True

if __name__ == "__main__":
    build_graph(FILE_PATH, PRINT_GRAPH)

    while True:
        try:
            print(
                "Hello Fireman, Im an intelligent agent pathfinder who can give you directions with minimal cost."
            )
            print("Please write exit to terminate the program.\n")

            departure = (
                input("Please enter the city of departure:")
                .strip()
                .replace(" ", "")
                .lower()
            )

            if inputExit(departure):
                break

            arrival = (
                input("Please enter the city of arrival:")
                .strip()
                .replace(" ", "")
                .lower()
            )

            if inputExit(arrival):
                break

            os.system("cls" if os.name == "nt" else "clear")
            print("1 = BFS\n2 = DFS\n3 = UCS")
            method = int(input("Which method?"))

            match method:
                case 1:
                    breadth_first_search(cities, departure, arrival)
                case 2:
                    depth_first_search(cities, departure, arrival)
                case 3:
                    uniform_cost_search(cities, departure, arrival)
                case default:
                    pass

        except CityNotFoundError as cne:
            print("City named", cne.args[0], "couldn't be found.")


"""
too much comments aaaaaa
https://www.youtube.com/watch?v=Bf7vDBBOBUA
"""
