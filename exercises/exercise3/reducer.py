#!/usr/bin/python
import sys
maxSale = -1
oldKey = None
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue
    thisKey, thisSale = data_mapped
    thisSale = float(thisSale)
    if oldKey and oldKey != thisKey:
        print (oldKey + "\t" + str(maxSale))
        oldKey = thisKey
        maxSale = thisSale
    else:
        if thisSale > maxSale:
            maxSale = thisSale
    oldKey = thisKey
if oldKey != None:
    print (oldKey + "\t" + str(maxSale))