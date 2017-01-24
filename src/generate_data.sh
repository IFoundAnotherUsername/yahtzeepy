#!/bin/bash

games=$1

for i in $(seq 1 $games)
do
   python3 main.py -f ./data --id "$i"
   echo "$i"
done
