#!/usr/bin/python
import sys
total = 0
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue
    total += float(data_mapped[1])
print ("TOTAL_ABSOLUTO" + "\t" + str(total))

