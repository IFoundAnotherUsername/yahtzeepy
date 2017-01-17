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


def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

SIDES_PER_DIE = 6

def dice_to_dice_counts(dice):
    return [dice.count(x + 1) for x in range(SIDES_PER_DIE)]

def dice_counts_to_dice(dice_counts):
    dice = []
    for i, x in enumerate(dice_counts):
        for _ in range(x):
            dice.append(i + 1)
    return dice

class YahtzeeScoresheet:
    def __init__(self):
        self.score_names = (
            'ones',
            'twos',
            'threes',
            'fours',
            'fives',
            'sixes',
            'bonus', # sum >= 63 => 35
            'three_of_a_kind', # sum o dice
            'four_of_a_kind', # sum o dice
            'small_straight', # 30
            'large_straight', # 40
            'full_house', # 25
            'chance', # sum o dice
            'yahtzee', # 50
        )
        self.scores = range(len(self.score_names))




class YahtzeePlayer:

    def __init__(self, player_index): # keep_decision_function, assign_decision_function):
        self.player_index = player_index

    def keep_dice(self, dice_counts):
        """
        returns new dice counts for kept dice
        """
        print('testing keep for {}...'.format(dice_counts))
        return dice_counts[:]

    def assign_dice(self, dice_counts):
        print('testing assign for {}...'.format(dice_counts))
        print(dice_counts_to_dice(dice_counts))
        return True


class YahtzeeGame:

    def __init__(self, dice_count=5, rethrow_count=2, player_count=2):
        self.dice_count = dice_count
        self.rethrow_count = rethrow_count
        self.player_count = player_count
        self.round = 0
        self.players = [YahtzeePlayer(x) for x in range(player_count)]
        print('Game started\n')

    def roll(self, dice_count):
        print('rolling {}...'.format(dice_count))
        dice = roll_dice(self.dice_count)
        print('rolled {}'.format(dice))
        return dice

    def roll_until_final_dice(self, player, dice):
        for i in range(self.rethrow_count):
            # rethrow non-kept
            kept_dice = player.keep_dice(dice_to_dice_counts(dice))
            if len(kept_dice) == self.dice_count:
                print('kept all dice!')
                break # if all kept, jump to assign
            else:
                print('keeping {}'.format(kept_dice))
                rethrow_num = self.dice_count - len(kept_dice)
                print('rethrowing {}...'.format(rethrow_num))
                new_dice = roll_dice(rethrow_num)
                print('got {}'.format(new_dice))
                dice = kept_dice + new_dice
                print('now having {}'.format(dice))
        return dice

    def update(self):
        print('round {} start'.format(self.round))

        for player in self.players:
            print('player {}'.format(player.player_index + 1))

            # throw initial
            dice = self.roll(self.dice_count)

            final_dice = self.roll_until_final_dice(player, dice)

            # assign dice
            player.assign_dice(dice_to_dice_counts(final_dice))


        print('round {} end\n'.format(self.round))
        self.round += 1

        if self.round > 5:
            print('Game over')
            return False
        else:
            return True

dice_count = 6
rethrow_count = 3
player_count = 2
game = YahtzeeGame(dice_count, rethrow_count, player_count)

while game.update():
    pass
