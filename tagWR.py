#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 23:41:00 2015

@author: Tony
"""

try:
    rests, tags, mapfile = 0, 0, 0
    rests = open("Rchainlist.txt", 'r', encoding='latin-1')
    tags = open("foodtags.txt", 'r', encoding='utf-8')
    
    restlist = rests.readlines()
    taglist = tags.readlines()
    rests.close()
    tags.close()
    rests, tags = 0, 0
    restlist = [r.strip() for r in restlist]

    results = dict()
    print("For each tag, input the restaurant name")
    for tag in taglist:
        notsafe, add = 1, 1
        while(notsafe):
            rname = input("%s: "%(tag.strip()))
            if (rname.strip()=='xskip'):
                notsafe, add = 0, 0
                print("skipped")
            elif ("-rx" in rname.strip()):
                notsafe, rname = 0, rname.strip("-rx")
            elif (rname.strip() in restlist): 
                notsafe = 0
            else: 
                print("Not in list, try again")
        if (add):
            results[tag.strip()] = rname.strip()
    
    mapfile = open("mappings.txt", 'w', encoding='utf-8')
    mapfile.write(str(results))
    mapfile.close()
    mapfile = 0
    
except IOError as e:
    print("%s: try again"%(e))
    
finally:
    if (rests!=0):
        rests.close()
    if (tags!=0):
        tags.close()
    if (mapfile!=0):
        mapfile.close()