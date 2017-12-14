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
import os,time
import sys

# Creating Output folder.
if (os.path.exists("Output")):
    delete1 = str('rm -r Output')
    delete2 = str('rm logs.txt')
    os.system(delete1)
    os.system(delete2)
    os.makedirs("Output")
else:
    os.makedirs("Output")

# Making a log file.
logs = open('logs.txt','w')
logs.write("Following links threw errors. Have to do manually -->\n\n")

# Printing unecessary information to look cool.
print ("\t\t>>>>>> Amazon Review Scraper <<<<<<")
print ("\t\t>>>>>> Author : ConanKapoor  <<<<<<\n")

# Taking url as input.
url = input(">>> Please Enter the REVIEW URL for the product : \n    ")
tempurl= url.split("/")
ProductName = tempurl[3]
tempurl = tempurl[0:6]
tempurl = '/'.join(tempurl)

# Scraping needed data.
modifiedurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + "1" +"?showViewpoints=1&pageNumber=" + "1"
time.sleep(1)
print ("\n\n>>> Modified url for getting Pagination Data - \n    %s"%(modifiedurl))
request = urllib.request.Request(modifiedurl)
response = urllib.request.urlopen(request)

# Using BeautifulSoup to parse html object response.
soup = BeautifulSoup(response.read(),"lxml")

# Using BeautifulSoup to find number of Paginations.
Pagination = soup.find("ul", {"class": "a-pagination"})
Pages = Pagination.find_all("li",{"class": "page-button"})
LastPage = int(Pages[len(Pages)-1].text)

############ Now LastPage contains the number of links to scrape ##############
###################### Main Scraping Logic Starts Below #######################
print ("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print ("\t\t>>>>>> Review Scraping Starts  <<<<<<")
print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
print (">>> Product Name - %s "%(ProductName))
print(">>> No of Review Pages - %s\n"%(LastPage))

for linkno in range(1,LastPage+1):
    # try:
    # Making custom URL.
    print("\n>>> Scraping Review Page - %s"%(linkno))
    newurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + str(linkno) +"?showViewpoints=1&pageNumber=" + str(linkno)
    print("    Link - %s"%(newurl))

    # Collecting html content.
    request = urllib.request.Request(newurl)
    response = urllib.request.urlopen(request)

    # Using BeautifulSoup to parse html object response.
    soup = BeautifulSoup(response.read(),"lxml")

    # Collecting Reviews.
    ReviewList = soup.find("div",{"id": "cm_cr-review_list"})
    Reviews = soup.find_all("div",{"class":"a-section review"})

    # Scraping different features from all reviews.
    for review in Reviews:
        # Scraping Author.
        AuthorHTML = review.find("a",{"data-hook":"review-author"})
        Author = AuthorHTML.text

        # Scraping Rating.
        RatingHTML = review.find("span",{"class": "a-icon-alt"})
        Rating = int(RatingHTML.text[0])

        # Scraping Date.
        DateHTML = review.find("span",{"data-hook":"review-date"})
        Date = DateHTML.text[3:]

        # Scraping Attribute (if there)
        AttributeHTML = review.find("a",{"data-hook":"format-strip"})
        Attribute = AttributeHTML.text

        # Printing Data
        print("\n    Author : %s"%(Author))
        print("    Rating : %s"%(Rating))
        print("    Date   : %s\n"%(Date))
        if Attribute is not None:
            print("    Attribute Available : Yes")
            print("    Attribute   : %s\n"%(Attribute))
        else:
            print("    Attribute Available : No\n")
        time.sleep(3000)

    # except Exception:
    #     print("\t>!>!> Exceptioncaught - skipping to next link.(Check logs.txt)\n")
    #     newurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + str(linkno) +"?showViewpoints=1&pageNumber=" + str(linkno)
    #     logs.write("Exception error - %s \n\n" %(newurl))
    #     pass

logs.close()
