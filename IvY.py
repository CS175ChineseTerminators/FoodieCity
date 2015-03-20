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
from state2abbr import abbr
from InstagramData import InstaData
from tag2name import tagnames

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
        
    def matches(self, option="", lookback=0):
        """Options: c=basic count function
                    d= selective predictor
        """
        if (option=="c"):
            instaData = self.instaCount()
            try:
                results, broken = [], 0
                for key in instaData:
                    if (instaData[key][0]):
                        city, state = key.split(',')
                        tag = instaData[key][0].strip("#")
                        YKey = city+abbr[state]
                        YKey = YKey.replace(' ','')
                        if (YKey in self.YData):
                            current = self.YData[YKey][0]
                            rest = tagnames[tag]                        
                            if (current[0]==rest):
                                results.append(1)
                            else:
                                results.append(0)
                                print("%s vs. %s"%(current[0], rest))
                        else:
                            print("what?%s"%(YKey))
                    else:
                        results.append(0)
                        broken += 1
                print("Option {}".format(option))
                percent = sum(results)/len(results)
                end = "{}/{} matches, {}%".format(sum(results), len(results), percent*100)
                print(end)
                print("%s broken, instagram did not return any results in current timeframe"%(broken))
            except IOError as e:
                print(e)
        elif (option=="d"): #select within top 5
            self.instaPredict(lookback=lookback)
        else:
            print("No Option")
            return 0
        
    def instaCount(self, option=0):
        """Compares and return"""
        data = self.sumAllCount(self.ISents, option)
        top = dict()
        for line in data:
            most = (None, -1)
            for tag in data[line]:
                if (data[line][tag] > most[1]):
                    most = (tag, data[line][tag])
            top[line.split(maxsplit=1)[1]] = most
        return top
        
    def sumAllCount(self, IData, option=0):
        """Takes IData structure dict[key]=([],[target])
        Calculates a weight for each based on sentiments and subjectiveness        
        """
        results = dict()
        for key in IData:
            results[key] = self.sumSentiments(IData[key], option)
        return results
            
    def sumSentiments(self, datalist, option=0) -> list:
        """Takes a list of (comment, (sent,subject)) returns weight"""
        results = dict()
        for i in range(len(datalist[0])):
            if (option):
                weight = datalist[1][i][0]*5 + 5.0
            else:
                weight = datalist[1][i][0]*5 + datalist[1][i][1]*3 + 3.0
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
        
    def instaPredict(self, lookback=0):
        """Predicts within the top 5 from the Yelp data using Instagram Data"""
        results, recentmatches, cityoptions, broken = [], [], dict(), 0
        instaData = self.instaCount(option=1)
        for key in instaData:
            if (instaData[key][0]):
                city, state = key.split(',')
                tag = instaData[key][0].strip("#")
                YKey = city+abbr[state]
                YKey = YKey.replace(' ','')
                if (YKey in self.YData):
                    current = self.YData[YKey][0]
                    cityoptions = [[City[0], City[2]] for City in self.YData[YKey]]
                    rest = tagnames[tag]
                    for i in range(len(cityoptions)):
                        if (cityoptions[i][0]==rest):
                            newrating = instaData[key][1]+cityoptions[1][1]*3
                            cityoptions[i].append(newrating)
                        else:
                            cityoptions[i].append(cityoptions[1][1]*3)
                        if (lookback):
                            for match in recentmatches:
                                if (cityoptions[i][0] == match):
                                    cityoptions[i][2] += 10.0
                    cityoptions.sort(reverse=True, key=lambda x:x[2])
                    if (cityoptions[0][0]==current[0]):
                        results.append(1)
                    else:
                        results.append(0)
                    if (lookback):
                        if (len(recentmatches)==5): recentmatches.pop(0)
                        recentmatches.append(current[0])
            else:
                results.append(0)
                broken += 1
        print("Option d")
        percent = sum(results)/len(results)
        end = "{}/{} matches, {}%".format(sum(results), len(results), percent*100)
        print(end)
        print("%s broken, instagram did not return any results in current timeframe"%(broken))

        
            
            
            