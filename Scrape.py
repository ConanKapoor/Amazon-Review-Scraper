#########################################
# Author - Shivam Kapoor (kapoor.shivam88@gmail.com)
#
# A simple script made in a day to scrape Amazon reviews for future NLP
# related research.
#
# Github : https://github.com/ConanKapoor/Amazon-Review-Scraper
#########################################

# Importing Essesnsials.
from bs4 import BeautifulSoup
from pyfiglet import Figlet
import urllib.request
import xlsxwriter
import time
import sys
import os

try:
    # Creating Output folder.
    if (os.path.exists("Output")):
        delete1 = str('rm -r Output')
        os.system(delete1)
        os.makedirs("Output")
    else:
        os.makedirs("Output")

    # Opening File to read URLs. Write URLs in links.txt
    with open("links.txt", "r") as link:
        content = link.read().splitlines()

    # Making a log file.
    logs = open('Output/logs.txt','w')
    logs.write("Following links threw errors. Have to do manually -->\n\n")

    for link in range(0,len(content)):
        count = 0

        # Printing unecessary information for 'wanna be cool' people.
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = Figlet(font='slant')
        print (banner.renderText('Amazon Scraper'))
        print (">>>>>> Amazon Review Scraper <<<<<<")
        print (">>>>>> Author : ConanKapoor  <<<<<<\n")

        # Printing unecessary information for 'wanna be cool' people #2.
        print (">>> Reading Data from links.txt - successful")
        print (">>> Log file made (logs.txt) - Check in Output/logs.txt")

        # Printing unecessary information for 'wanna be cool' people #3
        print ("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print (">!>!> NOTE : Add more links by copying REVIEW links to links.txt")
        print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        print (">>> Scraping Page link(from links.txt) - %s"%(link+1))

        # Taking url from links.txt
        url = content[link]
        tempurl= url.split("/")
        ProductName = tempurl[3]
        tempurl = tempurl[0:6]
        tempurl = '/'.join(tempurl)

        # Printing Product Name
        time.sleep(1)
        print (">>> Product Name - %s \n"%(ProductName))

        # Scraping needed data.
        modifiedurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + "1" +"?showViewpoints=1&pageNumber=" + "1"
        time.sleep(1)
        print (">>> Getting Pagination Data ")
        request = urllib.request.Request(modifiedurl)
        response = urllib.request.urlopen(request)

        # Using BeautifulSoup to parse html object response.
        soup = BeautifulSoup(response.read(),"lxml")

        # Using BeautifulSoup to find number of Paginations.
        Pagination = soup.find("ul", {"class": "a-pagination"})
        if Pagination is not None:
            Pages = Pagination.find_all("li",{"class": "page-button"})
            LastPage = int(Pages[len(Pages)-1].text.replace(",",""))
        else:
            LastPage = 1

        print (">>> Done!!!")
        time.sleep(1)
        print (">>> No of Review Pages - %s\n"%(LastPage))
        time.sleep(1)
        print (">>> Contacting server ...")
        time.sleep(1)
        print (">>> Successful!!!\n")
        time.sleep(1)

        ############ Now LastPage contains the number of links to scrape ##############
        ###################### Main Scraping Logic Starts Below #######################
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print ("\t\t>>>>>> Review Scraping Starts  <<<<<<")
        print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # Initiating XLSX file
        filepath = 'Output/Reviews-'+ ProductName +'.xlsx'
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Author', bold)
        worksheet.write('B1', 'Rating', bold)
        worksheet.write('C1', 'Date', bold)
        worksheet.write('D1', 'Attribute Available', bold)
        worksheet.write('E1', 'Attribute', bold)
        worksheet.write('F1', 'Verified Purchase', bold)
        worksheet.write('G1', 'Image Present', bold)
        worksheet.write('H1', 'Top 10 Reviewer', bold)
        worksheet.write('I1', 'Heading', bold)
        worksheet.write('J1', 'Description', bold)
        worksheet.write('K1', 'Number of Comments', bold)
        worksheet.write('L1', 'Upvotes', bold)

        rows = 1
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
                for review in Reviews:
                    count=count+1
                    print("    >>> Scraping Review number - %s"%(count))

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

                    # Review Heading.
                    HeadingHTML = review.find("a",{"data-hook":"review-title"})
                    Heading = HeadingHTML.text

                    # Is image present in review?
                    ImageHTML = review.find("div",{"class":"review-image-tile-section"})

                    # Top 10 reviewer?
                    TopHTML = review.find("span",{"class":"c7yTopDownDashedStrike"})

                    # Review Description
                    DescriptionHTML = review.find("span",{"data-hook":"review-body"})
                    Description = DescriptionHTML.text

                    # Number of comments
                    CommentsHTML = review.find("span",{"class":"review-comment-total"})
                    Comments = int(CommentsHTML.text)

                    # Number of upvotes
                    UpvotesHTML = review.find("span",{"class":"review-votes"})

                    # Uncomment below to Print Data into Terminal
                    '''
                    print("\n        Author : %s"%(Author))
                    print("        Rating : %s"%(Rating))
                    print("        Date   : %s\n"%(Date))

                    if Attribute is not None:
                        print("        Attribute Available : Yes")
                        print("        Attribute   : %s\n"%(Attribute))
                    else:
                        print("        Attribute Available : No\n")

                    if VerifiedHTML is not None:
                        if VerifiedHTML.text == "Verified Purchase" or TopHTML is not None:
                            print("        Verified Purchase : Yes\n")
                        else:
                            print("        Verified Purchase : No\n")
                    else:
                        print("        Verified Purchase : No\n")

                    if ImageHTML is not None:
                        print("        Image Present : Yes\n")
                    else:
                        print("        Image Present : No\n")

                    if TopHTML is not None:
                        print("        Top 10 Reviewer : Yes\n")
                    else:
                        print("        Top 10 Reviewer : No\n")

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
                    '''

                    # Saving Data into XLSX
                    worksheet.write(rows, 0, Author)
                    worksheet.write(rows, 1, Rating)
                    worksheet.write(rows, 2, Date)

                    if Attribute is not None:
                        worksheet.write(rows, 3, "Yes")
                        worksheet.write(rows, 4, Attribute)
                    else:
                        worksheet.write(rows, 3, "No")
                        worksheet.write(rows, 4, None)

                    if VerifiedHTML is not None:
                        if VerifiedHTML.text == "Verified Purchase" or TopHTML is not None:
                            worksheet.write(rows, 5, "Yes")
                        else:
                            worksheet.write(rows, 5, "No")
                    else:
                        worksheet.write(rows, 5, "No")

                    if ImageHTML is not None:
                        worksheet.write(rows, 6, "Yes")
                    else:
                        worksheet.write(rows, 6, "No")

                    if TopHTML is not None:
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
                        worksheet.write(rows, 11, int(Upvotes[6]))

                    rows = rows + 1

            except Exception:
                print("\t>!>!> Exceptioncaught - skipping to next link.(Check logs.txt)")
                print("              Most Probably Network error.")
                print("              Rerouting to next link.\n")
                newurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + str(linkno) +"?showViewpoints=1&pageNumber=" + str(linkno)
                logs.write("Exception error - %s \n\n" %(newurl))
                pass

        # Closing the workbook and logs
        print("\n>>> Total number of reviews scraped - %s\n"%(count))
        logs.write("End of logs - Complete Scraping done")
        workbook.close()
        time.sleep(5)

    logs.close()

except Exception:
    print("    >!>!> Exceptioncaught - skipping to next link.(Check logs.txt)")
    print("          Most Probably Network error.")
    print("          Rerouting to next link.\n")
    # newurl = tempurl + "/ref=cm_cr_arp_d_paging_btm_" + str(linkno) +"?showViewpoints=1&pageNumber=" + str(linkno)
    logs.write(" Outer Exception error.\n\n")
    pass

except KeyboardInterrupt:
    print("\n\n>>> Interrupt received! Exiting cleanly...")
    print(">>> Total number of reviews scraped - %s\n"%(count))
    logs.write("End of logs - Abruptly Ended")
    workbook.close()
    logs.close()
    sys.exit()

############################### END OF SCRIPT :) ##############################
