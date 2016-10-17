#!/usr/bin/python3
import re

with open("input.txt") as f:
    for line in f:
        #print(line)
        operation,value = re.split('\s',line)[:2]
        print(operation,value)
