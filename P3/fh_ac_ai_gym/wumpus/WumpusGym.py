import gym
from gym import error, spaces, utils
from gym.utils import seeding
from fh_ac_ai_gym.wumpus.WumpusWorld import Wumpus_World
from fh_ac_ai_gym.wumpus.WorldState import World_State, Action


class WumpusWorldEnv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self, size=4):
        self._world = Wumpus_World(size)
        self.action_space = [0,1,2,3,4,5]   # possible actions

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
        self.sentences = {('-P00',),('-W00',)}  # possible actions
        self.firstMethod = False

    def hornClauses(self, e1, e2, x, y):
        list1 = []
        list2 = []

        list1.append(e1 + str(x) + str(y))
        list2.append(e1 + str(x) + str(y))

        if(x < self.size - 1):
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
            self.sentences.add((tuple(list1), (e2 + str(x) + str(y + 1), )))
            if(y > 0):
                self.sentences.add((tuple(list1), (e2 + str(x) + str(y - 1), )))

        if (y > 0):
            copy_first.append('-' + e1 + str(x) + str(y - 1))
            self.sentences.add((tuple(copy_first), (e2 + str(x) + str(y - 1), )))
            if(y < self.size - 1):
                self.sentences.add((tuple(copy_first), (e2 + str(x) + str(y + 1), )))

        if (x < self.size - 1):
            copy_second.append('-' + e1 + str(x + 1) + str(y))
            self.sentences.add((tuple(list1), (e2 + str(x + 1) + str(y), )))
            if (y < self.size - 1):
                self.sentences.add((tuple(list1), (e2 + str(x + 1) + str(y), )))

        if (x > 0):
            copy_second.append('-' + e1 + str(x - 1) + str(y))
            self.sentences.add((tuple(copy_second), (e2 + str(x - 1) + str(y), )))
            if (x < self.size - 1):
                self.sentences.add((tuple(copy_second), (e2 + str(x + 1) + str(y), )))

    #def tell(self, perception):


    #def ask(self):
