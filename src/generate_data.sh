#!/bin/bash

games=$1

for i in $(seq 1 $games)
do
   python3 main.py -f /Users/elias/GitHub/yahtzeepy/data --id "$i" -l 30
   echo "$i"
done