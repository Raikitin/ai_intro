from graph import *
import queue


def create_graph() -> Graph:
    return Graph(['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
                  'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi', 'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
                 [
                     ('Or', 'Ze', 71),
                     ('Or', 'Si', 151),
                     ('Ne', 'Ia', 87),
                     ('Ze', 'Ar', 75),
                     ('Ia', 'Va', 92),
                     ('Ar', 'Si', 140),
                     ('Ar', 'Ti', 118),
                     ('Si', 'Fa', 99),
                     ('Si', 'Ri', 80),
                     ('Fa', 'Bu', 211),
                     ('Va', 'Ur', 142),
                     ('Ri', 'Pi', 97),
                     ('Ri', 'Cr', 146),
                     ('Ti', 'Lu', 111),
                     ('Lu', 'Me', 70),
                     ('Me', 'Dr', 75),
                     ('Dr', 'Cr', 120),
                     ('Cr', 'Pi', 138),
                     ('Pi', 'Bu', 101),
                     ('Bu', 'Gi', 90),
                     ('Bu', 'Ur', 85),
                     ('Ur', 'Hi', 98),
                     ('Hi', 'Ef', 86)
                 ])


def get_node_from_edge(self: Edge, start: Node) -> Node:
    return self.end if self.start == start else self.end


def bfs(graph: Graph, start: str, end: str):
    root_node = next(i for i in graph.nodes if i.name == start)
    my_queue: list[tuple[int, Node, Node | None]] = [(0, root_node, None)]
    while my_queue:
        next_node: tuple[int, Node, Node] = my_queue.pop(0)
        if next_node[1].parent == 0:
            next_node[1].parent = next_node[2]
            next_node[1].value = next_node[0]
            if next_node[1].name == end:
                value: int = next_node[0]
                print(next_node[1].name, end=" ")
                to_print: Node = next_node[1].parent
                while to_print is not None:
                    value += to_print.value
                    print("<-", to_print.name, end=" ")
                    to_print = to_print.parent
                print("\n", value)
            for edge in next_node[1].edges:
                other: Node = get_node_from_edge(edge, next_node[1])
                if other.parent == 0:
                    my_queue.append((edge.value, other, next_node[1]))


def dfs(graph: Graph, start: str, end: str):
    root_node = next(i for i in graph.nodes if i.name == start)
    stack: list[tuple[int, Node, Node]] = [(0, root_node, None)]
    while stack:
        next_node: tuple[int, Node, Node] = stack.pop()
        if next_node[1].parent == 0:
            next_node[1].parent = next_node[2]
            next_node[1].value = next_node[0]
            if next_node[1].name == end:
                value: int = next_node[0]
                print(next_node[1].name, end=" ")
                to_print: Node = next_node[1].parent
                while to_print is not None:
                    value += to_print.value
                    print("<-", to_print.name, end=" ")
                    to_print = to_print.parent
                print("\n", value)
            for edge in next_node[1].edges:
                other: Node = get_node_from_edge(edge, next_node[1])
                if other.parent == 0:
                    stack.append((edge.value, other, next_node[1]))


def ucs(graph: Graph, start: str, end: str):
    root_node = next(i for i in graph.nodes if i.name == start)
    my_queue = queue.PriorityQueue()
    my_queue.put((0, root_node, None))
    while my_queue.qsize() > 0:
        next_node: tuple[int, Node, Node] = my_queue.get()
        if next_node[1].parent == 0:
            next_node[1].parent = next_node[2]
            next_node[1].value = next_node[0]
            if next_node[1].name == end:
                print(next_node[1].name, end=" ")
                to_print: Node = next_node[1].parent
                while to_print is not None:
                    print("<-", to_print.name, end=" ")
                    to_print = to_print.parent
                print("\n", next_node[0])
            for edge in next_node[1].edges:
                other: Node = get_node_from_edge(edge, next_node[1])
                if other.parent == 0:
                    my_queue.put((edge.value + next_node[0], other, next_node[1]))


print("bfs:")
romania = create_graph()
bfs(romania, 'Bu', 'Ti')

print("\ndsf:")
dfs(create_graph(), 'Bu', 'Ti')

print("\nucs:")
ucs(create_graph(), 'Bu', 'Ti')
