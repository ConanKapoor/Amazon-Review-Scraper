# Author - Shivam Kapoor (kapoor.shivam88@gmail.com)

#########################################
'''
A simple script made in a day to scrape Amazon reviews for future NLP
related research.
Github : https://github.com/ConanKapoor/Amazon-Review-Scraper
'''
#########################################

# Importing Essesnsials.
from bs4 import BeautifulSoup
import urllib.request
import os,tldextract
import sys

# Creating Output folder
if (os.path.exists("Output")):
    delete1 = str('rm -r Output')
    delete2 = str('rm logs.txt')
    os.system(delete1)
    os.system(delete2)
    os.makedirs("Output")
else:
    os.makedirs("Output")

# Making a log file
logs = open('logs.txt','w')
logs.write("Following links threw errors. Have to do manually -->\n\n")

# Taking url as input
url = input("Please Enter the REVIEW URL for the product : ")
tempurl = url.split("/")
tempurl = tempurl[0:6]
tempurl = '/'.join(tempurl)

# Scraping needed data
modifiedurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + "1" +"?showViewpoints=1&pageNumber=" + "1"
request = urllib.request.Request(modifiedurl)
response = urllib.request.urlopen(request)

# Using BeautifulSoup to parse html object response.
soup = BeautifulSoup(response.read(),"html5lib")
