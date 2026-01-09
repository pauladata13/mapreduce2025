# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
count = 0
oldKey = None
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue
    thisKey, thisCount = data_mapped
    thisCount = int(thisCount)
    if oldKey and oldKey != thisKey:
        print (oldKey + "\t" + str(count))
        oldKey = thisKey
        count = thisCount
    else:
        count += thisCount
    oldKey = thisKey
if oldKey != None:
    print (oldKey + "\t" + str(count))
