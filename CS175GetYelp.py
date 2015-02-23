# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 14:13:09 2015

@author: Tony
"""

import rauth, tearYelpKeys, sys

def get_search_parameters(area, name=''):
    """Search params, will be only for restaurants in this project"""
    params = {}
    if (name): params["term"] = name 
    else: params["term"] = "restaurant"
    params["location"] = area
    return params
    
def get_results(params):
    """Obtain information from Yelp"""
    consumer_key = tearYelpKeys.CKey
    consumer_secret = tearYelpKeys.CSecret
    token = tearYelpKeys.Token
    token_secret = tearYelpKeys.TSecret
    
    session = rauth.OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = token,
        access_token_secret = token_secret)
        
    request = session.get("http://api.yelp.com/v2/search", params=params)
    
    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()
    return data
    
def get_restaurantList(location, restaurant):
    """ Obtain list of restaurants in a dictionary[name]=info """
    param = get_search_parameters(location, restaurant)
    results = get_results(param)
    return results['businesses']

    
if __name__ == "__main__":
    if (len(sys.argv)<3):
        print("""Usage:\n\tCS175GetYelp.py "<city,state>" "<restaurant>" """)
    else:
        location, restaurant = sys.argv[1], sys.argv[2].replace(' ', '-')
#        rList = get_restaurantList(location, restaurant)
        rList = []
        city = sys.argv[1].split(",")[0].strip()
        total = get_restaurantList(location, restaurant)
        for restaurant in total:
            if (restaurant['location']['city']==city):
                rList.append(restaurant)
        if (len(rList)==0):
            rList=total
        total = None
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