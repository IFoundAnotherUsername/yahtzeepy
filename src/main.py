"""
main
"""

import random

# import tensorflow as tf

# hello = tf.constant('Hello, TensorFlow!')
# sess = tf.Session()
# print(sess.run(hello))
# a = tf.constant(10)
# b = tf.constant(32)
# print(sess.run(a + b))

def throw_dice(num_dice):
    return tuple(map(lambda x: random.randint(1, 6), range(num_dice)))


class YahtzeeScoresheet:
    def __init__(self):
        self.score_names = (
            'ones',
            'twos',
            'threes',
            'fours',
            'fives',
            'bonus',
            'pairs',
            'two_pairs',
            'three_of_a_kind',
            'four_of_a_kind',
            'small_straight',
            'large_straight',
            'full_house',
            'chance',
            'yahtzee',
        )
        self.scores = range(len(self.score_names))


class YahtzeePlayer:

    def __init__(self, player_index):
        self.player_index = player_index
        pass

    def select_dice(self, dice):
        """
        returns a list of indices of kept dice
        """
        kept_indices = []
        for (die_index, die) in enumerate(dice):
            if die == 6:
                kept_indices.append(die_index)
            else:
                pass

        return kept_indices

    def is_satisfied(self, with_dice, with_throw_number):
        """
        returns true if not wanting to reroll
        """
        return with_throw_number == 2


class YahtzeeGame:

    def __init__(self, dice_count=5, player_count=2):
        self.dice_count = dice_count
        self.player_count = player_count
        self.round = 0
        self.players = list(map(lambda x: YahtzeePlayer(x), range(player_count)))
        print('Game started\n')

    def rethrow(self, keep_array):
        pass

    def update(self):

        print('round {} start'.format(self.round))

        for player in self.players:
            print('player {}'.format(player.player_index + 1))

            # throw dice
            print('throwing...')
            dice = throw_dice(self.dice_count)
            print(dice)

            # assign if satisfied
            if player.is_satisfied(dice, 1):
                # TODO assign score
                continue
            else:
                # else keep
                dice = tuple(map(lambda x: dice[x], player.select_dice(dice)))
                print('keeping {}'.format(dice))

            # rethrow
            rethrow_count = 5 - len(dice)
            print('rethrowing {}...'.format(rethrow_count))
            new_dice = throw_dice(rethrow_count)
            print('got {}'.format(new_dice))
            dice += new_dice
            print('now having {}'.format(dice))

            # assign if satisfied
            if player.is_satisfied(dice, 1):
                # TODO assign score
                continue
            else:
                # else keep
                dice = tuple(map(lambda x: dice[x], player.select_dice(dice)))
                print('keeping {}'.format(dice))

            # rethrow
            rethrow_count = 5 - len(dice)
            print('rethrowing {}...'.format(rethrow_count))
            new_dice = throw_dice(rethrow_count)
            print('got {}'.format(new_dice))
            dice += new_dice
            print('now having {}'.format(dice))

            # TODO assign score

        print('round {} end\n'.format(self.round))
        self.round += 1

        if self.round > 5:
            print('Game over')
            return False
        else:
            return True

dice_count = 5
player_count = 2
game = YahtzeeGame(dice_count, player_count)

while game.update():
    pass
