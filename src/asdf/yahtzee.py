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
DICE_COUNT = 5

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

        self.action_space = Discrete(LEN_SCORE_NAMES)
        AVAILABLE_NO = 0
        AVAILABLE_YES = 1
        self.observation_space = Box(AVAILABLE_NO, AVAILABLE_YES, LEN_SCORE_NAMES + DICE_COUNT)

    def _seed(self, seed=None):
        self.np_radom, seed_1 = gym.utils.seeding.np_random(seed)
        seed_2 = gym.utils.seeding.hash_seed(seed_1 + 1) % 2**31
        return [seed_1, seed_2]

    def _reset(self):
        self.score = YahtzeeScoreTable()
        self.dice = self.roll_all()
        self.state = self.get_state()
        return self.state

    def _close(self):
        self.score = None

    def _render(self, mode="human", close=False):
        print(repr(self.score))
        print("State:", self.get_state(), "Reroll", NM_REROLLS - self.nb_reroll)


    def roll_all(self):
        return [random.randint(1, 6) for i in range(DICE_COUNT)]

    def get_state(self):
        return self.score.as_observation() + self.dice

    def _step(self, action):

        if self.score.is_completed():
            reward = self.score.total()
            return self.state, 0, True, {}

        assert self.action_space.contains(action)

        # reward = self.act(action)
        score_cell = self.score.table[action]
        available = score_cell.available
        matches_dice = score_cell.validator(self.dice)

        if available and matches_dice:
            score_cell.value = score_cell.score(self.dice)
            self.score.table[action] = score_cell
            self.dice = self.roll_all()
            reward = 1
            return self.get_state(), reward, False, {'found_match': True}
        elif available:
            score_cell.value = 0
            self.score.table[action] = score_cell
            self.dice = self.roll_all()
            reward = 0
            return self.get_state(), reward, False, {'found_match': False}
        else:
            self.dice = self.roll_all()
            reward = -1
            return self.get_state(), reward, False, {}

    def total_score(self):
        bonus = 0
        sub_total = 0
        for i in range(7, 12):
            sub_total += self.score.table[i].value
        if sub_total > 62:
            bonus = 36
        return self.score.total() + bonus



