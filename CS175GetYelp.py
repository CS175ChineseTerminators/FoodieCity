# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 14:13:09 2015

@author: Tony
"""

import rauth, tearYelpKeys

# city, long, lat, rating(float)

def get_search_parameters(city):
    """Search params, will be only for restaurants in this project"""
    params = {}
    params["term"] = "restaurant"
#    params["location"] = "Irvine, CA"
    params["location"] = city
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
    
if __name__ == "__main__":
    param = get_search_parameters("Irvine, CA")
    results = get_results(param)
    # results keys = {businesses, total, region}
    Yelp_Restaurants = results["businesses"]
    # Yelp_Restaurants keys = {rating, rating_img_url, is_claimed,
    # review_count, url, rating_img_url_large, display_phone,
    # image_url, location, is_closed, categories, phone, name, url}
    # Keys are all in string
    
#    print(get_results(param))