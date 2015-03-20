#! /bin/usr/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 14:13:09 2015

@author: Tony
"""

import rauth, tearYelpKeys, sys, ast, operator
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import glob
import os

class GetYelp(object):

    def __init__(self):
        self._CKey = tearYelpKeys.CKey
        self._CSecret = tearYelpKeys.CSecret
        self._Token = tearYelpKeys.Token
        self._TSecret = tearYelpKeys.TSecret
        

    def get_search_parameters(self, area, name=''):
        """Search params, will be only for restaurants in this project"""
        params = {}
        if (name): params["term"] = name
        else: params["term"] = "restaurant"
        params["location"] = area
        return params
        
    def get_results(self, params):
        """Obtain information from Yelp"""
        
        session = rauth.OAuth1Session(
            consumer_key = self._CKey,
            consumer_secret = self._CSecret,
            access_token = self._Token,
            access_token_secret = self._TSecret)
            
        request = session.get("http://api.yelp.com/v2/search", params=params)
        
        #Transforms the JSON API response into a Python dictionary
        data = request.json()
        session.close()
        return data
        
    def get_restaurantList(self, location, restaurant):
        """ Obtain list of restaurants in a dictionary[name]=info """
        param = self.get_search_parameters(location, restaurant)
        results = self.get_results(param)
        return results['businesses']     
        
    def filterRList(self, RList, city):
        """ Filters RList to only restaurants with that certain City """
        results = []
        for r in RList:
            if (r['location']['city']==city.strip()):
                results.append(r)
        return results

    def read_infoList(self, file=""):
        """ Supply this function a file argument, containing all restaurant
            that would be interesting
        """
        infoList = []
        try:
            if (file):
                with open(file, 'r', encoding="latin-1") as F:
                    for line in F:
                        infoList.append(line.strip())
        except IOError as E:
            print("%s\nUnopenable restaurant chain file"%(E))
            
        return infoList   
        
    def getRestaurantsByCity(self, restaurantList, city):
        """ Returns a dict of all chain restaurants in city specified """
        RC = dict()  # RC[restaurant name] = restaurant info
        C = city.split(',')[0]
        for r in restaurantList:
            if (r in RC):
                RC[r].append(self.filterRList(
                            self.get_restaurantList(city.strip(), r.replace(' ','-')), C))
            else:
                RC[r] = [self.filterRList(
                            self.get_restaurantList(city.split(',')[0].strip(), r.replace(' ','-')), C)]
                            
        return RC
        
    def getAllCity(self, restaurantList, cityList):
        """ Return a dict, dict[city] = (dict[rest. name] = rest. info """
        RCityList = []
        for city in cityList:
            RCityList.append(self.getRestaurantsByCity(restaurantList, city))
        return RCityList
        
    def extractYData(self, filename=""):
        """Pass a text file containing Yelp Data, return in dict form"""
        result = None
        try:
            with open(filename, 'r', encoding="latin-1") as f:
                text = f.read()
            result = ast.literal_eval(text)
            if (result):
                return result
            else:
                raise ValueError("ValueError")
        except IOError as e:
            print("%s: Invalid filename provided"%(e))
        except ValueError as e:
            print("%s: Read Error, try again"%(e))
        except SyntaxError as e:
            with open(filename, 'r', encoding="utf-8") as f:
                text = f.read()
                result = ast.literal_eval(text)
            if (result):
                return result
    
    def getRatings(self, filename=""):
        """Returns a dict[restaurant] = [ratings] """
        if (filename):
            data = self.extractYData(filename)
            ratings = dict()
            for key in data.keys():
                ratings[key] = []
                for i in range(len(data[key][0])):
                    current = data[key][0][i]
                    if (current['name']==key):
                        ratings[key].append((current['rating'], current["review_count"]))
            return ratings
            
    def getHighestCount(self, citydatafile=""):
        """Returns a dict[restaurant]=[total ratings_count]"""
        if (citydatafile):
            data = self.extractYData(citydatafile)
            toplist = []
            for key in data.keys():
                totalreview, ratings = 0, []
                if (len(data[key][0])):
                    for i in range(len(data[key][0])):
                        current = data[key][0][i]
                        if (current['name']==key):
                            totalreview += current["review_count"]
                            ratings.append(current['rating'])
                    if (totalreview):
                        avg = sum(ratings)/len(ratings)
                        toplist.append((key, totalreview, avg))
            toplist.sort(reverse=True, key=lambda x:x[1])
            return toplist[0:5]
        return None
        
    def getAllTop(self, filedir="", filelist=""):
        """Checks file data dir, gets all top restaurtant"""
        if (filedir and filelist):
            sys.path.append(filedir)
            with open(filelist, 'r', encoding="latin-1") as f:
                files = f.read().split("\n")
            results = dict()
            for file in files:
                if (file):
                    results[file.strip(".txt")] = self.getHighestCount(filedir+file)
            return results
        else:
            return "Need both a valid filedir and filelist"
                
#####         
# Functions below, Author: Raymond Lee
###
    def readAllFiles(self, path=""):
        """Returns all the files in the YData Folder
            Change File Path 
        """
        #allFiles= glob.glob("/Users/Raymond/anaconda/lib/YData/*")
        #return allFiles
        
        cities = []
        if not (path):
            path = "/Users/Raymond/anaconda/lib/YData/"
        
        for (root, dirs, f) in os.walk(path):
            for filename in f:
                if filename.endswith(".txt"):
                    filename = os.path.join(root, filename)
                    filename = "/".join(filename.split("/")[5:7])
                    #city_state = os.path.splitext(filename)[0]
                    cities.append(filename)
                    
        return cities
        
    def listOfChains(self):
        subprocess.Popen("rm Rchainlist.txt", stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, shell=True).communicate()
        
        infile = urlopen('http://en.wikipedia.org/wiki/List_of_restaurant_chains_in_the_United_States')
        page = infile.read()
        soup = BeautifulSoup(page)
        write_to_file = []
        table = soup.find("table", {"class": "wikitable sortable"})
        table.encode('utf-8')
        
        with open("Rchainlist.txt", 'w') as f:
            for row in table.finAll("tr"):
                cells = row.findAll("td")
                if (len(cells)==4):
                    city = cells[0].find(text=True)
                    f.write(city)
                    write_to_file.append(city)
        
        return write_to_file
        
    def topRatings(self, filename=""):
        """Returns a dict[restaurant] = [ratings] """
        if (filename):
            data = self.extractYData(filename)
            filename  = "/".join(filename.split("/")[1:2])
            city_state = os.path.splitext(filename)[0]
            state = city_state[-2:]
            
            new_ratings = dict()
            review_counts = dict()
            restaurants = self.listOfChains()
            printed_ratings = dict()
            for key in data.keys():
                new_ratings[key] = []
                review_counts[key] = []
                printed_ratings[key] = []
                
                for i in range(len(data[key][0])):
                    current = data[key][0][i]
                    one = current['rating']
                    two = current['review_count']
                    three = current['name']
                    four = current['location']['state_code']
                    number = (one * two)
                    if((key == three) and (two > 1)):
                        review_counts[key].append((two))
                        new_ratings[key].append((number))
                if(len(review_counts[key]) != 0):
                    if((key in restaurants) and (state == four)): 
                        number_of_restaurants = len(data[key][0])
                        number_of_restaurants= number_of_restaurants/1000
                        answer = sum(new_ratings[key])/sum(review_counts[key]) + number_of_restaurants
                        printed_ratings[key].append((answer))
                else:
                    answer = 0
                    printed_ratings[key].append((answer))
               
            sorted_dict = sorted(printed_ratings.items(), key=operator.itemgetter(1), reverse = True)[:50]
            return sorted_dict
        
    def extractAllData(self):
        print("Made it!")
        allFiles = self.readAllFiles()
        print(allFiles)
        final = dict()
        for key in range(len(allFiles)):
            city = self.topRatings(allFiles[key])
            final[allFiles[key]] = city
        return final
    
if __name__ == "__main__":
    if (len(sys.argv)<3):
        print("""Usage:\n\tCS175GetYelp.py "<city,state>" "<restaurant>" """)
    else:
        getYelp = GetYelp()
        location, restaurant = sys.argv[1], sys.argv[2].replace(' ', '-')
        rList = []
        city = sys.argv[1].split(",")[0].strip()
        total = getYelp.get_restaurantList(location, restaurant)
        for restaurant in total:
            if (restaurant['location']['city']==city):
                rList.append(restaurant)
        if (len(rList)==0):
            rList=total
        print("List of restaurant dictionaries saved into var rList")
