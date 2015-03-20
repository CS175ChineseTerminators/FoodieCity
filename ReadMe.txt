Code Doc.

Tony Ear

CS175GetYelp.py - contains methods that calls Yelp API, pulls the data, filters the data,
		  pulls Yelp ratings, give average ratings of multiple restaurants, return 
		  highest review count among restaurants in a city, extract Yelp data from 
		  other text files and read list text files

InstagramData.py - Contains methods that deal with the already mined Instagram Data.
		   Reads the instagram files filtered by our set of tags we deem as interesting.
		   Collects tags from the posts, counts them, returns the max, and 
		   utilizes the TextBlob library to perform a sentiment analysis. Can 
		   be automated to collection by text files of all cities

IvY.py -  Contains methods to run comparisons using the Instagram Data vs the Yelp Data
	  Starts by with calculating and parsing the instagram data by comments and hashtags,
	  adds sentiments and weights from those sentiments to sum up and use as the Instagram
	  Data to be used in the comparisons. It then matches using options, using a regular
	  simple count algorithm, and a narrow selection algorithm.


abr2states.py - simple script, maps state abbriviation to full name

state2abbr.py - reverse of above, maps full name to abbriviation

tag2name.py - simple mapping, hashtag -> restaurant name

tagWR.py - script to help create the above mapping, associates tag to restaurant