from collections import defaultdict, deque
from Rover.world.abstract.orientation import directions


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.ev3operations = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance, ev3instructions=None):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance
        self.ev3operations[(from_node, to_node)] = ev3instructions
        self.ev3operations[(to_node, from_node)] = opposite(ev3instructions)

#TODO : Intergrate with ev3 instructions
def opposite(instructions):
    pass

def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    full_instructions = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        prev_destionation = _destination
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)
    for a in range(len(list(full_path)) - 1):
        instructions = graph.ev3operations[(list(full_path)[a], list(full_path)[a + 1])]
        full_instructions.append(instructions)

    return visited[destination], origin,destination, list(full_path), list(full_instructions)

if __name__ == '__main__':
    from world.ev3controls import movements
    graph = Graph()
    paths = {}
    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        graph.add_node(node)

    graph.add_edge('A', 'B', 10, ['X','Y','Z'] )
    graph.add_edge('A', 'C', 20,['X','YZ'])
    graph.add_edge('B', 'D', 15, ['AX','Y'])
    graph.add_edge('C', 'D', 30, ['X','Y'])
    graph.add_edge('B', 'E', 50, ['ZX','Y'])
    graph.add_edge('D', 'E', 30,['X','DY'])
    graph.add_edge('E', 'F', 5, ['FX','Y'])
    graph.add_edge('F', 'G', 2, ['X','Y'])

    for x in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        paths[x] ={}
        for y in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            if x!=y:
                paths[x][y]=(shortest_path(graph,x,y))
                #print(shortest_path(graph, x, y))

    print(paths)

    current_location = 'A'
    employee_location = 'D'
    instructions_dictionary = {'move_forward': movements.move_foward , 'move_backward': ,'turn_left': ,'turn_right': }
    print(paths[current_location][employee_location])
    if current_location != employee_location:
        instructions_list = paths[current_location][employee_location][4]
        instructions_to_be_executed = [instr for list in instructions_list for instr in list]
        for a in instructions_to_be_executed:
            print('Executing instruction',a)
            # eval(a)
    else:
        print("Invalid Destination Location")