import graph


class Queue:
    procedure = "lifo"
    structuredData = list()

    def __init__(self, procedure):
        if (procedure in {'lifo', 'fifo', 'prio'}):
            self.procedure = procedure
            self.structuredData = list()
        else:
            print("Invalid procedure")

    def push(self, item):
        if (self.procedure == "lifo"):
            self.structuredData.insert(0, item)
        elif (self.procedure == "fifo"):
            self.structuredData.append(item)
        elif (self.procedure == "prio"):
            index = 0
            while (index < len(self.structuredData) and int(self.structuredData[index].value) < int(item.value)):
                index += 1
            if (index >= len(self.structuredData)):
                self.structuredData.append(item)
            else:
                self.structuredData.insert(index, item)

    def pop(self):
        if (not self.structuredData):
            print("Queue is empty")
            return None
        else:
            return self.structuredData.pop(0)

    def peek(self):
        return self.structuredData[0]

    # def contains(self, item):
    #     for element in self.structeredData:
    #         if(item == element):
    #             return True
    #     return False

    def contains(self, item):
        return item in self.structuredData

    def empty(self):
        return (not self.structuredData)

    def print(self):
        for item in self.structuredData:
            print(item, end=' , ')
        print('')


class Node:
    start = None
    end = None
    romania = None
    explored = None
    visitable = None
    path = None

    def __init__(self):
        self.explored = set()
        self.path = []
        self.romania = romania = graph.Graph(['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
                                              'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
                                              'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
                                             [
                                                 ('Or', 'Ze', 71), ('Or', 'Si', 151),
                                                 ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
                                                 ('Ia', 'Va', 92), ('Ar', 'Si', 140),
                                                 ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
                                                 ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
                                                 ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
                                                 ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
                                                 ('Lu', 'Me', 70), ('Me', 'Dr', 75),
                                                 ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
                                                 ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
                                                 ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
                                                 ('Hi', 'Ef', 86)
                                             ])

    def updateStart(self, node):
        if(node.start == []):
            node.start = [node.end]
        else:
            node.start.append(node.end)

    def updatePath(self, path):
        for node in path:
            self.path.append(node)

    # TODO not marked adj for BFS and UCS
    def notMarkedAdjacent(self, nedge):
        for edges in self.romania.nodes:
            if edges.name == nedge:
                source = edges.name
                adjacents = []
                for edge in edges.edges:
                    if(source == edge.end.name and not edge.start.name in self.explored.name):
                        adjacents.append(graph.Edge([edge.end.name, edge.start.name, edge.value]))
                    elif(source == edge.start.name and not edge.end.name in self.explored):
                        adjacents.append(graph.Edge([edge.start.name, edge.end.name, edge.value]))
                return adjacents
        return []


    def printExplored(self):
        for i, node in enumerate(self.explored):
            print(i+1, ': Explored: ', node)

    def printPath(self):
        for i, node in enumerate(self.path):
            print(i+1, ': Path: ', node)
        print("Cost: ", self.getPathCost())

    def getPathCost(self):
        cost = 0
        for i in range(0, len(self.path) - 1):
            cost += self.romania.getWeight(self.path[i], self.path[i+1])
        return cost

    # TODO BFS UCS Test

    def BFS(self, start, end):
        self.explored = set()
        self.path = []
        self.visitable = Queue('fifo')
        self.visitable.push(graph.Edge([[], start, 0]))

        while(True):
            node = None
            while(not self.visitable.empty()):
                node = self.visitable.pop()
                if(not node in self.explored):
                    break
            else:
                    return False

            self.explored.add(node.end)

            if(node.end == end):
                node.start.append(node.end)
                self.updatePath(node.start)
                return True

            self.updateStart(node)

            for adjacent in self.notMarkedAdjacent(node.end):
                self.visitable.push(graph.Edge([node.start.copy(), adjacent.end, adjacent.value]))


    def DFS(self, start, end):
        self.explored = {start}
        self.path = [start]
        self.DFS_rec(self.romania.getNode(start), start, end)

    def DFS_rec(self, node, start, end):
        if(node.name == end):
            return True
        for adjacent in self.romania.getAdjacent(node):
            if(not adjacent.name in self.explored):
                self.explored.add(adjacent.name)
                self.path.append(adjacent.name)
                if(self.DFS_rec(adjacent, start, end)):
                    return True
                self.path.pop()
                self.explored.remove(adjacent.name)
        if(node.name == start):
            return False

    def UCS(self, start, end):
        self.visitable = Queue('prio')
        self.explored = set()
        self.visitable.push(graph.Edge([[], start, 0]))
        self.path = []

        while(True):
            if(self.visitable.empty()):
                return False

            edge = self.visitable.pop()
            self.explored.add(edge.end)

            if(edge.end == end):
                edge.start.append(edge.end)
                self.updatePath(edge.start)
                #self.pathCost = edge.value
                return True

            self.updateStart(edge)

            for adjacent in self.notMarkedAdjacent(edge.end):
                self.visitable.push(graph.Edge([edge.start.copy(), adjacent.end, adjacent.value + edge.value]))



test = Node()
test.BFS('Bu', 'Ti')
test.printPath()
test.DFS('Bu', 'Ti')
test.printPath()
test.UCS('Bu', 'Ti')
test.printPath()
#print("test")