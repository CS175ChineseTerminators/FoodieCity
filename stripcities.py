# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 00:52:42 2015

@author: Tony
"""

class StripCities(object):
    
    def __init__(self, filestr):
        try:
            self.file = []
            with open(filestr, 'r') as f:
                for line in f.read().split('\n'):
                    self.file.append(line)
        except EnvironmentError as e:
            raise e
        
    def parse(self):
        lines = []
        for line in self.file:
            build = ' '.join(line.split()[1:-2])
            lines.append(build)
        return lines
        
if __name__ == "__main__":
    import sys
    if (len(sys.argv)==2):
        SC = StripCities(sys.argv[1])
        p = SC.parse()
    else:
        print("Please provide one text file")
        