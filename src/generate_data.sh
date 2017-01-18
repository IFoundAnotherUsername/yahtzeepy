#!/bin/bash

games=$1

for i in $(seq 1 $games)
do
   python3 main.py -f /Users/elias/GitHub/yahtzeepy/data
   echo "$i"
done