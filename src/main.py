"""
main
"""

import sys, getopt
import random

# import tensorflow as tf

# hello = tf.constant('Hello, TensorFlow!')
# sess = tf.Session()
# print(sess.run(hello))
# a = tf.constant(10)
# b = tf.constant(32)
# print(sess.run(a + b))

SIDES_PER_DIE = 6

def roll_dice(num_dice):
    return [random.randint(1, SIDES_PER_DIE) for _ in range(num_dice)]

def dice_to_dice_counts(dice):
    return [dice.count(x + 1) for x in range(SIDES_PER_DIE)]

def dice_counts_to_dice(dice_counts):
    dice = []
    for i, x in enumerate(dice_counts):
        for _ in range(x):
            dice.append(i + 1)
    return dice

# If no dice of the appropriate type are found you will strike = 0p

def score_ones(dice_counts):
    return 1 * dice_counts[0]

def score_twos(dice_counts):
    return 2 * dice_counts[1]

def score_threes(dice_counts):
    return 3 * dice_counts[2]

def score_fours(dice_counts):
    return 4 * dice_counts[3]

def score_fives(dice_counts):
    return 5 * dice_counts[4]

def score_sixes(dice_counts):
    return 6 * dice_counts[5]

def score_type(dice_counts, type):
    return type * dice_counts[type-1]

def score_pair(dice_counts):
    for i, x in enumerate(dice_counts):
        if x == 2: score_type(dice_counts, i+1)
    return 0

def score_3_kind(dice_counts):
    for i, x in enumerate(dice_counts):
        if x == 3: score_type(dice_counts, i+1)
    return 0

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
        self.options = {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0, 'fives': 0, 'sixes': 0, 'pair': 0, '3-kind': 0}
        self.score = 0

    def random_assign(self, dice_counts):
        open_options = []

        # print('options: ' , str(self.options))
        for k, v in self.options.items():
            if v == 0:
                open_options.append(k)
        choice = random.choice(open_options)
        scoring_options = {
            'ones' : score_ones(dice_counts),
            'twos' : score_twos(dice_counts),
            'threes' : score_threes(dice_counts),
            'fours' : score_fours(dice_counts),
            'fives' : score_fives(dice_counts),
            'sixes' : score_sixes(dice_counts),
            'pair' : score_pair(dice_counts),
            '3-kind' : score_3_kind(dice_counts)
        }
        self.options[choice] = 1
        print('Picking', choice)
        return scoring_options[choice]

    def keep_dice(self, dice_counts):
        """
        returns new dice counts for kept dice
        """
        print('testing keep for {}...'.format(dice_counts))
        return [min(x, 1) for x in dice_counts]

    def assign_dice(self, dice_counts):
        print('testing assign for {}...'.format(dice_counts))
        print(dice_counts_to_dice(dice_counts))
        round_score = self.random_assign(dice_counts)
        print('scored', round_score)
        self.score += round_score
        return True



class YahtzeeGame:

    def __init__(self, dice_count, rethrow_count, player_count, round_count, inputfile, outputfile):
        self.dice_count = dice_count
        self.rethrow_count = rethrow_count
        self.player_count = player_count
        self.round = 0
        self.players = [YahtzeePlayer(x) for x in range(player_count)]
        self.round_count = round_count
        self.inputfile = inputfile
        self.outputfile = outputfile

        print('Game started\n')

    def roll(self, dice_count):
        print('rolling {}...'.format(dice_count))
        dice = roll_dice(self.dice_count)
        print('rolled {}'.format(dice))
        return dice

    def roll_until_final_dice(self, player, dice):
        for i in range(self.rethrow_count):
            # rethrow non-kept
            kept_dice = dice_counts_to_dice(player.keep_dice(dice_to_dice_counts(dice)))
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

        if self.round > self.round_count:
            for player in self.players:
                print('player {}'.format(player.player_index + 1), ': {}'.format(player.score), 'points')
            print('Game over')
            return False
        else:
            return True


def main(argv):

    # Defaults
    dice_count = 3
    rethrow_count = 1
    player_count = 2
    round_count = 7
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"h:d:t:p:r:i:o:",["dice=","throws=","players=","rounds=","ifile=","ofile="])
    except getopt.GetoptError:
        print('main.py -d <dice> -t <throws> -p <players> -r <rpunds> -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <dice> -t <throws> -p <players> -r <rpunds> -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-d", "--dice"):
            dice_count = int(arg)
        elif opt in ("-t", "--throws"):
            rethrow_count = int(arg)
        elif opt in ("-p", "--players"):
            player_count = int(arg)
        elif opt in ("-r", "--rounds"):
            round_count = int(arg)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Will start a game with', dice_count, ' dice, ', player_count, 'players.' )

    game = YahtzeeGame(dice_count, rethrow_count, player_count, round_count, inputfile, outputfile)

    while game.update():
        pass


if __name__ == "__main__":
   main(sys.argv[1:])