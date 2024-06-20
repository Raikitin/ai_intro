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

        if (x > 0):
            list1.append('-' + e1 + str(x - 1) + str(y))

        if (y < self.size - 1):
            list2.append('-' + e1 + str(x) + str(y + 1))

        if (y > 0):
            list2.append('-' + e1 + str(x) + str(y - 1))

        copy_first = list1.copy()
        copy_second = list2.copy()

        if (y < self.size - 1):
            list1.append('-' + e1 + str(x) + str(y + 1))
            self.sentences.add((tuple(list1), (e2 + str(x) + str(y + 1),)))
            if (y > 0):
                self.sentences.add((tuple(list1), (e2 + str(x) + str(y - 1),)))

        if (y > 0):
            copy_first.append('-' + e1 + str(x) + str(y - 1))
            self.sentences.add((tuple(copy_first), (e2 + str(x) + str(y - 1),)))
            if (y < self.size - 1):
                self.sentences.add((tuple(copy_first), (e2 + str(x) + str(y + 1),)))

        if (x < self.size - 1):
            copy_second.append('-' + e1 + str(x + 1) + str(y))
            self.sentences.add((tuple(list1), (e2 + str(x + 1) + str(y),)))
            if (y < self.size - 1):
                self.sentences.add((tuple(list1), (e2 + str(x + 1) + str(y),)))

        if (x > 0):
            copy_second.append('-' + e1 + str(x - 1) + str(y))
            self.sentences.add((tuple(copy_second), (e2 + str(x - 1) + str(y),)))
            if (x < self.size - 1):
                self.sentences.add((tuple(copy_second), (e2 + str(x + 1) + str(y),)))

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
                for item in self.premises(current):  # TODO: def premises()
                    count[item[0]] -= 1
                    if (count[item[0]] == 0):
                        for add in self.conclusion(item):  # TODO def conclusion()
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

    #def resolution():

    #def tell(self, perception):

    #def ask(self):
