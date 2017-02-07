import random
import gym
from gym.spaces import Discrete, Box

SCORE_NAMES = {
    'Yahtzee': 0x00,       # 50
    'Chance': 0x01,        # sum(dice)
    'LargeStraight': 0x02, # 40
    'SmallStraight': 0x03, # 30
    'FullHouse': 0x04,     # 25
    'FourOfAKind': 0x05,   # sum(dice)
    'ThreeOfAKind': 0x06,  # sume(dice)
    'Sixs': 0x07,          # 0, 6, 12, 18, 24 0r 30
    'Fives': 0x08,         # 0, 5, 10, 15, 20 0r 25
    'Fours': 0x09,         # 0, 4,  8, 12, 16 0r 20
    'Threes': 0x0A,        # 0, 3,  6,  9, 12 0r 15
    'Twos': 0x0B,          # 0, 2,  4,  6,  8 0r 10
    'Ones': 0x0C           # 0, 1,  2,  3,  4 0r  5
}

LEN_SCORE_NAMES = len(SCORE_NAMES)
NM_REROLLS = 2
AVAILABLE = -1

def _sum(x, v):
    return sum([i for i in x if i==v])

def _count(x):
    result = [0] * 6
    for i in x:
        result[i-1] += 1
    return result

def _largestraight_validator(x):
    return x.count(1) == 5 and (x[0] == 0 or x[5] == 0)

def _smallstraight_validator(x):
    return (x[2] > 0 and x[3] > 0) and ((x[0] > 0 and x[1] > 0)  or \
           (x[1] > 0 and x[4] > 0) or (x[4] > 0 and x[5] > 0))

class ScoreCell(object):
    def __init__(self, _id, name, value=AVAILABLE, score=sum, validator=sum):
        self._id = _id
        self.name = name
        self.value = value
        self.score = score
        self.validator = validator

    @property
    def available(self):
        return self.value == AVAILABLE

    def __repr__(self):
        return "\n{0:>2}{1:>15}: {2:>4}".format(self._id, self.name, self.value)



class YahtzeeScoreTable(object):

    def __init__(self):
        self.table = {}
        self.add_cell('Yahtzee', lambda x: 50, lambda x: 5 in _count(x))
        self.add_cell('Chance')

        self.add_cell('LargeStraight', lambda x: 40, lambda x: _largestraight_validator(_count(x)))
        self.add_cell('SmallStraight', lambda x: 30, lambda x: _smallstraight_validator(_count(x)))
        self.add_cell('FullHouse', lambda x: 25, lambda x: 2 in _count(x) and 3 in _count(x))

        self.add_cell('FourOfAKind', validator=lambda x: 4 in _count(x) or 5 in _count(x))
        self.add_cell('ThreeOfAKind', validator=lambda x: 3 in _count(x) or 4 in _count(x) or 5 in _count(x))

        self.add_cell('Sixs', lambda x: _sum(x, 6), lambda x: 6 in x)
        self.add_cell('Fives', lambda x: _sum(x, 5), lambda x: 5 in x)
        self.add_cell('Fours', lambda x: _sum(x, 4), lambda x: 4 in x)
        self.add_cell('Threes', lambda x: _sum(x, 3), lambda x: 3 in x)
        self.add_cell('Twos', lambda x: _sum(x, 2), lambda x: 2 in x)
        self.add_cell('Ones', lambda x: _sum(x, 1), lambda x: 1 in x)


    def add_cell(self, name, score=sum, validator=sum):
        id_ = SCORE_NAMES[name]
        self.table[id_] = ScoreCell(id_, name, score=score, validator=validator)

    def total(self):
        return sum([self.table[i].value for i in range(LEN_SCORE_NAMES) if not self.table[i].available])

    def as_observation(self):
        table_state = [int(not self.table[i].available) for i in range(LEN_SCORE_NAMES)]
        return table_state

    def is_completed(self):
        return True not in [self.table[i].available for i in range(LEN_SCORE_NAMES)]

    def __repr__(self):
        txt = "\n{0:>2}{1:>10}{2:>6}".format("Decision", "sNames", "Score")
        txt += "\n=========================="
        for i in reversed(sorted(range(LEN_SCORE_NAMES))):
            txt += repr(self.table[i])
        txt += "\n=========================="
        return txt


class YahtzeeEnv(gym.Env):

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.score = None
        self.state = None
        self.nb_reroll = NM_REROLLS

        #An action is an integer in the interval [0, 31]. If bit
        #i (2**i) is on, this corresponds to rolling the ith die.
        self.action_space = Discrete(32)

        # dice
        self.observation_space = Box(1, 6, 5)

    def _seed(self, seed=None):
        self.np_radom, seed_1 = gym.utils.seeding.np_random(seed)
        seed_2 = gym.utils.seeding.hash_seed(seed_1 + 1) % 2**31
        return [seed_1, seed_2]

    def _reset(self):
        self.score = YahtzeeScoreTable()
        self.state = [random.randint(1, 6) for i in range(5)]
        return self.state

    def _close(self):
        self.score = None

    def _render(self, mode="human", close=False):
        print(repr(self.score))
        print("Dice:", self.state, "Reroll", NM_REROLLS - self.nb_reroll)

    def _step(self, action):

        if self.score.is_completed():
            reward = self.score.total()
            return self.state, 1, True, {}

        assert self.action_space.contains(action)

        reward = self.act(action)

        return self.state, reward, False, {}

    def act(self, action):
        newdice = []
        for i in range(5):
            mask = 2 ** i
            if action & mask == 0:
                newdice.append(self.state[i])
        dice_to_reroll = 5 - len(newdice)

        if dice_to_reroll:
            newdice.extend([random.randint(1, 6) for i in range(dice_to_reroll)])
            newdice.sort()
            self.state = newdice

        reward = self.random_best_score_from_available_cells(self.state)

        return reward

    def random_best_score_from_available_cells(self, return_max_score=True):
        reward = 0
        all_available = []
        valid_available = []

        for c in range(LEN_SCORE_NAMES):
            if self.score.table[c].available:
                all_available.append(c)
                if self.score.table[c].validator(self.state):
                    valid_available.append(c)

        if valid_available:
            if return_max_score:
                max_score = -1
                max_available = []
                for c in valid_available:
                    c_score = self.score.table[c].score(self.state)
                    if c_score > max_score:
                        max_score = c_score
                        max_available.append(c)

                random.shuffle(max_available)
                cell = random.choice(max_available)
            else:
                random.shuffle(valid_available)
                cell = random.choice(valid_available)

            i_should_score = random.randint(0, 1)
            if self.nb_reroll and not i_should_score:
                self.nb_reroll -= 1
            else:
                reward = self.score.table[cell].score(self.state)
                self.score.table[cell].value = reward
                self.nb_reroll = NM_REROLLS
                self.state = [random.randint(1, 6) for i in range(5)]
        else:
            if self.nb_reroll:
                self.nb_reroll -= 1
            else:
                random.shuffle(all_available)
                cell = random.choice(all_available)
                self.score.table[cell].value = reward
                self.nb_reroll = NM_REROLLS
                self.state = [random.randint(1, 6) for i in range(5)]

        return reward

    def total_score(self):
        bonus = 0
        sub_total = 0
        for i in range(7, 12):
            sub_total += self.score.table[i].value
        if sub_total > 62:
            bonus = 36
        return self.score.total() + bonus



