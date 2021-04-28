# doing necessary imports

from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
import pandas as pd
  # initialising the flask app with the name 'app'


  # obtaining the search string entered in the form
 # if there is a collection with searched keyword and it has records in it

dominos_url = "https://play.google.com/store/search?q=dominos%20app"  # preparing the URL to search the product on flipkart
uClient = uReq(dominos_url)  # requesting the webpage from the internet
DominosPage = uClient.read()  # reading the webpage
uClient.close()  # closing the connection to the web server
Dominos_html = bs(DominosPage, "html.parser")  # parsing the webpage as HTML
bigboxes = Dominos_html.findAll("div", {"class": "ImZGtf mpg5gc"})  # seacrhing for appropriate tag to redirect to the product link
#del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
box = bigboxes[0]  # taking the first iteration (for demo)
DominosLink = "https://play.google.com" + box.div.div.div.div.div.div.a['href']  # extracting the actual product link
DominosRes = requests.get(DominosLink)  # getting the product page from server
Dominos_html = bs(DominosRes.text, "html.parser")  # parsing the product page as HTML
commentboxes = Dominos_html.find_all('div',{"class": "zc7KVe"})  # finding the HTML section containing the customer comments


  # creating a collection with the same name as search string. Tables and Collections are analogous.
    # filename = searchString+".csv" #  filename to save the details
    # fw = open(filename, "w") # creating a local file to save the details
    # headers = "Product, Customer Name, Rating, Heading, Comment \n" # providing the heading of the columns
    # fw.write(headers) # writing first the headers to file
    # reviews = [] # initializing an empty list for reviews
    #  iterating over the comment section to get the details of customer and their comments
for commentbox in commentboxes:
  try:
    rating = commentbox.div.div.div.div.div.div['aria-label']
  except:
    rating = 'No Ratinf'
  try:
    Comment = commentbox.div.div.find_all('span', {'jsname': 'bN97Pc'}).text
  except:
    Comment = 'No Comment'

  mydict = {"Rating": rating, "Comments": Comment}

      # fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
    # saving that detail to a dictionary


      # insertig the dictionary containing the rview comments to the collection

df = pd.DataFrame(mydict)  # appending the comments to the review list
df.to_csv('DominosReviews.csv')



