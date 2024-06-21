import queue

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from fh_ac_ai_gym.wumpus.WumpusWorld import Wumpus_World
from fh_ac_ai_gym.wumpus.WorldState import World_State, Action


class WumpusWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, size=4):
        self._world = Wumpus_World(size)
        self.action_space = [0, 1, 2, 3, 4, 5]  # possible actions

    def step(self, action):
        done = self._world.exec_action(action)
        obs = self._world.get_observation()
        reward = self._world.get_reward()
        return obs, reward, not done, {"info", "no further information"}

    def reset(self):
        self._world.reset()
        return self._world.get_observation()

    def render(self, mode='human'):
        self._world.print()

    def close(self):
        print("Not necessary since no seperate window was opened")
        pass


# adding the knowledge base of the wumpus game here
# WorldEnv will need a few updates
class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.sentences = {('-P00',), ('-W00',)}  # possible actions
        self.firstMethod = False

    def conjuctionAdjacent(self, e, x, y):
        if (x < self.size - 1):
            self.sentences.add((e + str(x + 1) + str(y),))
        if (y < self.size - 1):
            self.sentences.add((e + str(x) + str(y + 1),))
        if (x > 0):
            self.sentences.add((e + str(x - 1) + str(y),))
        if (y > 0):
            self.sentences.add((e + str(x) + str(y - 1),))

    def disconjuctionAdjacent(self, e, x, y):
        disjunction = []
        if (x < self.size - 1):
            disjunction.append(e + str(x + 1) + str(y))
        if (y < self.size - 1):
            disjunction.append(e + str(x) + str(y + 1))
        if (x > 0):
            disjunction.append(e + str(x - 1) + str(y))
        if (y > 0):
            disjunction.append(e + str(x) + str(y - 1))
        self.sentences.add(tuple(disjunction))

    def hornClauses(self, e1, e2, x, y):
        list1 = []
        list2 = []

        list1.append(e1 + str(x) + str(y))
        list2.append(e1 + str(x) + str(y))

        if (x < self.size - 1):
            list1.append('-' + e1 + str(x + 1) + str(y))

        if (y < self.size - 1):
            list2.append('-' + e1 + str(x) + str(y + 1))

        if (x > 0):
            list1.append('-' + e1 + str(x - 1) + str(y))

        if (y > 0):
            list2.append('-' + e1 + str(x) + str(y - 1))

        copy_first = list1.copy()
        copy_second = list2.copy()

        if (x < self.size - 1):
            copy_second.append('-' + e1 + str(x + 1) + str(y))
            self.sentences.add((tuple(list1), (e2 + str(x + 1) + str(y),)))
            if (y < self.size - 1):
                self.sentences.add((tuple(list1), (e2 + str(x + 1) + str(y),)))

        if (y < self.size - 1):
            list1.append('-' + e1 + str(x) + str(y + 1))
            self.sentences.add((tuple(list1), (e2 + str(x) + str(y + 1),)))
            if (y > 0):
                self.sentences.add((tuple(list1), (e2 + str(x) + str(y - 1),)))

        if (x > 0):
            copy_second.append('-' + e1 + str(x - 1) + str(y))
            self.sentences.add((tuple(copy_second), (e2 + str(x - 1) + str(y),)))
            if (x < self.size - 1):
                self.sentences.add((tuple(copy_second), (e2 + str(x + 1) + str(y),)))

        if (y > 0):
            copy_first.append('-' + e1 + str(x) + str(y - 1))
            self.sentences.add((tuple(copy_first), (e2 + str(x) + str(y - 1),)))
            if (y < self.size - 1):
                self.sentences.add((tuple(copy_first), (e2 + str(x) + str(y + 1),)))

    def hornClausesAdjacent(self, t, p, x, y):
        if (x < self.size - 1):
            self.sentences.add(((p + str(x) + str(y),), (t + str(x + 1) + str(y),)))
        if (y < self.size - 1):
            self.sentences.add(((p + str(x) + str(y),), (t + str(x) + str(y + 1),)))
        if (x > 0):
            self.sentences.add(((p + str(x) + str(y),), (t + str(x - 1) + str(y),)))
        if (y > 0):
            self.sentences.add(((p + str(x) + str(y),), (t + str(x) + str(y - 1),)))

    def forwardChaining(self, query):  # 06 - 34
        count = {}  # a table, where count[c] is the number of the symbols in c’s premise
        inferred = {}  # a table, where inferred[s] is initially false for all symbols
        agenda = queue.Queue()  # a queue of symbols, initially known to be true in KB

        for item in self.sentences:
            if (len(item) == 1):
                agenda.put(item)
                inferred[item] = False
                if (item[0] == query):
                    return True
                if (item[0] == '-' + query):
                    return False
            else:
                for items in item:
                    inferred[items] = False
                count[item[0]] = 0
                for items in item[0]:
                    count[item[0]] += 1

        while not agenda.empty():
            current = agenda.get()
            if (current == (query,)):
                return True
            if (not inferred[current]):
                inferred[current] = True
                for item in self.premises(current):
                    count[item[0]] -= 1
                    if (count[item[0]] == 0):
                        for add in self.conclusion(item):
                            agenda.put(add)
        return False

    def premises(self, q):
        result = set()
        for item in self.sentences:
            if (len(item) == 2):
                for i in item[0]:
                    if ((i,) == q):
                        result.add(item[0])
                        break
        return result

    def conclusion(self, q):
        result = set()
        for item in self.sentences:
            if (len(item) == 2 and item[0] == q):
                result.add(tuple(item[1]))
        return result

    def resolution(self, query):  # 06 - 31
        query = query[1:] if (query[0] == '-') else ('-' + query)
        clauses = self.sentences.copy()
        clauses.add((query,))
        new = set()

        while (True):
            for i in range(len(clauses)):
                for j in range(len(clauses)):
                    if (i == j):
                        continue
                    c1 = list(clauses)[i]
                    c2 = list(clauses)[j]

                    if (isinstance(c1, str)):
                        c1 = (c1,)
                    if (isinstance(c2, str)):
                        c2 = (c2,)

                    resolvent = self.resolve(c1, c2)

                    if (() in resolvent and len(resolvent) == 1):
                        return True

                    new |= resolvent

                if (new <= clauses):
                    return False

                clauses |= new

    def resolve(self, c1, c2):
        result = set()
        combined = {c1} | {c2}
        for item1 in c1:
            for item2 in c2:
                if (item1 and item2 and item1 == '-' + item2 or item2 == '-' + item1):
                    for x in combined:
                        tmp = []
                        for y in x:
                            if (y != item1 and y != item2):
                                tmp.append(y)
                            if (len(tmp) == 0):
                                result.add(tuple(tmp))

        if (result):
            return result
        return combined

    def tell(self, perception):
        x = perception['x']
        y = perception['y']

        if (self.firstMethod):

            if (perception['breeze']):
                self.sentences.add(('B' + str(x) + str(y),))
                self.sentences.add(('-P' + str(x) + str(y),))
                self.disconjuctionAdjacent('P', x, y)
            else:
                self.sentences.add(('-B' + str(x) + str(y),))
                self.conjuctionAdjacent('-P', x, y)
            if (perception['stench']):
                self.sentences.add(('S' + str(x) + str(y),))
                self.sentences.add(('-W' + str(x) + str(y),))
                self.disconjuctionAdjacent('W', x, y)
            else:
                self.sentences.add(('-S' + str(x) + str(y),))
                self.conjuctionAdjacent('-W', x, y)

        else:
            if (x < self.size - 1):
                self.hornClauses('B', 'P', x + 1, y)
                self.hornClauses('S', 'W', x + 1, y)
            if (y < self.size - 1):
                self.hornClauses('B', 'P', x, y + 1)
                self.hornClauses('S', 'W', x, y + 1)
            if (x > 0):
                self.hornClauses('B', 'P', x - 1, y)
                self.hornClauses('S', 'W', x - 1, y)
            if (y > 0):
                self.hornClauses('B', 'P', x, y - 1)
                self.hornClauses('S', 'W', x, y - 1)
            if (perception['breeze']):
                self.sentences.add(('B' + str(x) + str(y),))
            else:
                self.sentences.add(('-B' + str(x) + str(y),))
                self.conjuctionAdjacent('-P', x, y)
            if (perception['stench']):
                self.sentences.add(('S' + str(x) + str(y),))
            else:
                self.sentences.add(('-S' + str(x) + str(y),))
                self.conjuctionAdjacent('-W', x, y)

    def ask(self, x,y):
        value = []

        if(self.firstMethod):
            if(self.resolution('P'+str(x)+str(y))):
                value.append('Pit')
            elif(not self.resolution('-P'+str(x)+str(y))):
                value.append('?Pit')
            if(self.resolution('W'+str(x)+str(y))):
                value.append('Wumpus')
            elif(not self.resolution('-W'+str(x)+str(y))):
                value.append('?Wumpus')
            if(len(value) == 0):
                value.append('OK')

        else:
            if(self.forwardChaining('P'+str(x)+str(y))):
                value.append('Pit')
            elif(not self.forwardChaining('-P'+str(x)+str(y))):
                value.append('?Pit')
            if(self.forwardChaining('W'+str(x)+str(y))):
                value.append('Wumpus')
            elif(not self.forwardChaining('-W'+str(x)+str(y))):
                value.append('?Wumpus')
            if(len(value) == 0):
                value.append('OK')
        return ','.join(value)
