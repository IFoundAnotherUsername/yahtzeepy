# yahtzeepy
Yahtzee bot in Python

## Overview
* main.py: Generic python implementation of yahtzee. You can any configure for any ruleset.

* generate_data.py: Generates test & training data by playing number of games and saving input & output files.

* Tensorflow configuration: TBD

## How to train neural nets

Start data generation by feeding number of iterations to the script
```
./generate_data.sh <number of iterations>
```

* Use training data from data/keeper to train a neural net on what dice to keep
* Use training data from data/placer to train a neural net on where to place dice



