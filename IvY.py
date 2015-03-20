#! /bin/usr/env python
# -*- coding: utf-8 -*-
"""
IvY
Instagram vs Yelp Data
Takes interesting data (already made before arriving to script) and
comparing them against each other

@author: Tony
"""

import ast, os, sys, re
from InstagramData import InstaData

class InstagramVYelp(InstaData):
    
    def __init__(self, YDataFile="topfive.txt", filedir="IData/"):
        try:
            super(InstagramVYelp, self).__init__()
            with open(YDataFile, 'r', encoding='utf-8') as f:
                data = f.read()
            self.YData = ast.literal_eval(data)
            sys.path.append(filedir)
            self.Ifilelist = os.listdir(filedir) #list of IData
            self.Ifilelist = [filedir+file for file in self.Ifilelist]
            self.ISents = self.getCityNSents(self.Ifilelist)
        except IOError as e:
            print("Did not open correctly %s"%(e))
        
    def compareCount(self):
        """Compares and return"""
        data = self.sumAllCount(self.ISents)
        top = dict()
        for line in data:
            most = (None, -1)
            for tag in data[line]:
                if (data[line][tag] > most[1]):
                    most = (tag, data[line][tag])
            top[line.split(maxsplit=1)[1]] = most
        return top
        
    def sumAllCount(self, IData):
        """Takes IData structure dict[key]=([],[target])
        Calculates a weight for each based on sentiments and subjectiveness        
        """
        results = dict()
        for key in IData:
            results[key] = self.sumSentiments(IData[key])
        return results
            
    def sumSentiments(self, datalist) -> list:
        """Takes a list of (comment, (sent,subject)) returns weight"""
        results = dict()
        for i in range(len(datalist[0])):
            weight = datalist[1][i][0]*5 + datalist[1][i][1]*3 + 2.5
            for tag in self.getTag(datalist[0][i]):
                if (tag in results):
                    results[tag] += weight
                else:
                    results[tag] = weight
            #results.append((self.getTag(datalist[0][i]), weight))
        return results
        
    def getTag(self, comment) -> str:
        """Takes an instagram comment, returns tag"""
        tags = re.findall(r'#[^#|\s]+', comment)
        results = []
        for tag in tags:
            if (tag[1].lower() in self.taglist):
                if (tag.strip("#").lower() in self.taglist[tag[1].lower()]):
                    results.append(tag)
        return results
        
    def comparePredict(self):
        """Uses a preidiction"""
        pass
    
    
    def hello(self):
        return self.ISents