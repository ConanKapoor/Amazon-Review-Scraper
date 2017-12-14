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
import xlsxwriter
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
LastPage = int(Pages[len(Pages)-1].text.replace(",",""))

############ Now LastPage contains the number of links to scrape ##############
###################### Main Scraping Logic Starts Below #######################
print ("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print ("\t\t>>>>>> Review Scraping Starts  <<<<<<")
print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
print (">>> Product Name - %s "%(ProductName))
print(">>> No of Review Pages - %s\n"%(LastPage))

# Initiating XLSX file
workbook = xlsxwriter.Workbook('Reviews.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Author', bold)
worksheet.write('B1', 'Rating', bold)
worksheet.write('C1', 'Date', bold)
worksheet.write('D1', 'Attribute Available', bold)
worksheet.write('E1', 'Attribute', bold)
worksheet.write('F1', 'Verified Purchase', bold)
worksheet.write('G1', 'Image Present', bold)
worksheet.write('H1', 'Heading', bold)
worksheet.write('I1', 'Description', bold)
worksheet.write('J1', 'Number of Comments', bold)
worksheet.write('K1', 'Upvotes', bold)

count = 1
for linkno in range(1,LastPage+1):
    try:
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
        rows = 1
        for review in Reviews:
            print("\n\n    >>> Scraping Review number - %s"%(count))
            count=count+1

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

            # Is purchase verified?
            VerifiedHTML = review.find("span",{"data-hook":"avp-badge"})
            Verified = VerifiedHTML.text

            # Review Heading.
            HeadingHTML = review.find("a",{"data-hook":"review-title"})
            Heading = HeadingHTML.text

            # Is image present in review?
            ImageHTML = review.find("div",{"class":"review-image-tile-section"})

            # Review Description
            DescriptionHTML = review.find("span",{"data-hook":"review-body"})
            Description = DescriptionHTML.text

            # Number of comments
            CommentsHTML = review.find("span",{"class":"review-comment-total"})
            Comments = CommentsHTML.text

            # Number of upvotes
            UpvotesHTML = review.find("span",{"class":"review-votes"})

            # Printing Data into Terminal
            print("\n        Author : %s"%(Author))
            print("        Rating : %s"%(Rating))
            print("        Date   : %s\n"%(Date))

            if Attribute is not None:
                print("        Attribute Available : Yes")
                print("        Attribute   : %s\n"%(Attribute))
            else:
                print("        Attribute Available : No\n")

            if Verified == "Verified Purchase":
                print("        Verified Purchase : Yes\n")
            else:
                print("        Verified Purchase : No\n")

            if ImageHTML is not None:
                print("        Image Present : Yes\n")
            else:
                print("        Image Present : No\n")

            print("        Heading  : %s"%(Heading))
            print("        Description  : %s\n"%(Description))
            print("        Number of Comments : %s"%(Comments))

            if UpvotesHTML is None:
                print("        Upvotes : 0")
            elif UpvotesHTML.text.split(" ")[6] == "One":
                print("        Upvotes : 1")
            else:
                Upvotes = UpvotesHTML.text
                Upvotes = Upvotes.split(" ")
                print("        Upvotes : %s"%(Upvotes[6]))

        # Saving Data into XLSX
        worksheet.write(rows, 1, Author)
        worksheet.write(rows, 2, Rating)
        worksheet.write(rows, 3, Date)

        if Attribute is not None:
            worksheet.write(rows, 4, "Yes")
            worksheet.write(rows, 5, Attribute)
        else:
            worksheet.write(rows, 4, "No")
            worksheet.write(rows, 5, None)

        if Verified == "Verified Purchase":
            worksheet.write(rows, 6, "Yes")
        else:
            worksheet.write(rows, 6, "No")

        if ImageHTML is not None:
            worksheet.write(rows, 7, "Yes")
        else:
            worksheet.write(rows, 7, "No")

        worksheet.write(rows, 8, Heading)
        worksheet.write(rows, 9, Description)
        worksheet.write(rows, 10, Comments)

        if UpvotesHTML is None:
            worksheet.write(rows, 11, 0)
        elif UpvotesHTML.text.split(" ")[6] == "One":
            worksheet.write(rows, 11, 1)
        else:
            Upvotes = UpvotesHTML.text
            Upvotes = Upvotes.split(" ")
            worksheet.write(rows, 11, Upvotes[6])

        rows = rows + 1

    except Exception:
        print("\t>!>!> Exceptioncaught - skipping to next link.(Check logs.txt)\n")
        newurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + str(linkno) +"?showViewpoints=1&pageNumber=" + str(linkno)
        logs.write("Exception error - %s \n\n" %(newurl))
        pass

# Closing the workbook and logs
workbook.close()
logs.close()
