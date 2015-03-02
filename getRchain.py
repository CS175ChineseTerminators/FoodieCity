import urllib
from bs4 import BeautifulSoup
import wikipedia
from urllib.request import urlopen
import subprocess

subprocess.Popen("rm Rchainlist.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()


infile = urlopen('http://en.wikipedia.org/wiki/List_of_restaurant_chains_in_the_United_States')
page = infile.read()
soup = BeautifulSoup(page)

table = soup.find("table", {"class": "wikitable sortable"})
table.encode('utf-8')

with open("Rchainlist.txt", 'w') as f:
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if (len(cells)==4):
            city = cells[0].find(text=True)
            f.write(city+"\n")


        
    

    
