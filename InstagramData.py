#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 01:29:55 2015

@author: Tony
"""

import re
from textblob import TextBlob


class InstaData(object):
    
    def __init__(self, hashtagfile="foodtags.txt"):
        """ init with hashtag files to get from future files """
        self.taglist = dict()
        try:
            with open(hashtagfile, 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    add = line.strip()
                    if (add[0] not in self.taglist):
                        self.taglist[add[0]] = [add.strip()]
                    else:
                        self.taglist[add[0]].append(add.strip())
        except IOError:
            print("Not a valid tag file")
    
    def getTagList(self):
        return self.taglist

    def readInstaFile(self, filename=""):
        """ Reads the file with information from instagram """
        if not (filename):
            return "No File Name Given"
        else:
            try:
                textlist = set()
                with open(filename, 'r', encoding="utf-8") as f:
                    for line in f.readlines():
                        if (self.filterInFile(line)):
                            textlist.add(line)
                return list(textlist)
            except IOError as e:
                return "%s: Could not open File"%(e)
    
    def filterInFile(self, data) -> bool:
        """Takes line, returns bool if contains a relevant hashtag"""
        if (not data):
            return False
        tags = re.findall(r'#[^#|\s]+', data)
        for hashtag in tags:
            tag = hashtag.strip('#')
            if (tag[0] in self.taglist):
                if (tag in self.taglist[tag[0]]):
                    return True
        return False
        
    def sentiment(self, text) -> (float, float):
        """Takes text, returns (polarity, subjectivity)"""
        if (not text):
            raise ValueError("Empty Text")
        data = TextBlob(text)
        return (data.sentiment.polarity, data.sentiment.subjectivity)
        
    def getSentimentList(self, textlist) -> list:
        """Takes a list of texts, returns list of sentiments"""
        sentiments = [self.sentiment(text) for text in textlist]
        return sentiments
            
    
if __name__ == "__main__":
    print("hello")