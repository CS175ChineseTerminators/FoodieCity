#! /bin/usr/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 14:13:09 2015

@author: Tony
"""

import rauth, tearYelpKeys, sys, ast

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
                with open(file, 'r') as F:
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
            with open(filename, 'r') as f:
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

    
if __name__ == "__main__":
    if (len(sys.argv)<3):
        print("""Usage:\n\tCS175GetYelp.py "<city,state>" "<restaurant>" """)
    else:
        getYelp = GetYelp()
        location, restaurant = sys.argv[1], sys.argv[2].replace(' ', '-')
#        rList = get_restaurantList(location, restaurant)
        rList = []
        city = sys.argv[1].split(",")[0].strip()
        total = getYelp.get_restaurantList(location, restaurant)
        for restaurant in total:
            if (restaurant['location']['city']==city):
                rList.append(restaurant)
        if (len(rList)==0):
            rList=total
#        total = None
        print("List of restaurant dictionaries saved into var rList")
#    Yelp_Restaurants = dict()
#    for r in results["businesses"]:
#        Yelp_Restaurants[r["name"]] = r
#    Yelp_Restaurants = results["businesses"]
    # Yelp_Restaurants keys = {rating, rating_img_url, is_claimed,
    # review_count, url, rating_img_url_large, display_phone,
    # image_url, location, is_closed, categories, phone, name, url}
    # Keys are all in string
    
#    print(get_results(param))