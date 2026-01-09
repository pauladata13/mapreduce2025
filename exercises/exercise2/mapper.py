#!/usr/bin/python
import sys
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    data = line.split("\t")
    if len(data) != 5: continue
    try:
        datetime, store, item, cost, payment = data
        float(cost)
    except ValueError: continue
    print (item + "\t" + cost)