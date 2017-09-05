
import urllib2
from bs4 import BeautifulSoup
import os

#User will input lat long and will have to round it to the correct DEM, so whatever position is inside the dem it will download that dem
latitude = 40
longitude = 124

resoultion = 13 #for 1/3 arc second data
kind = IMG #for .img files
location = 'n%sw%s' % (str(latitude), str(longitude))

URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/%s/%s/' % (str(resolution), str(kind))


page = urllib2.urlopen(URL)
soup = BeautifulSoup(page, "lxml")
div = str(soup.find('div', class_ = 'well'))
log = open("log.txt", "w")
log.write(div)
log.close()
f = open("log.txt")
lines = f.readlines()
line = lines[short_name_line]
short_name = line[short_name_shear:]
f.close()
os.remove("log.txt")
short_name = short_name.rstrip()
