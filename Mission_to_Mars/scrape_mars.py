#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from pprint import pprint
from selenium import webdriver
import requests as req
import time


# # NASA Mars News

# In[2]:


def scrape():
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')


# In[3]:


#Assign the text to variables that you can reference later.
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find
    news_date = soup.find('div', class_='list_date')
    time.sleep(1)
    news_date


    # In[4]:


    news_title = soup.find('div', class_='content_title').text
    news_title


    # In[5]:


    news_parag = soup.find('div', class_='article_teaser_body')
    news_parag


    # # JPL Mars Space Images - Featured Image

    # In[6]:


    #Visit the url for JPL Featured Space Image.
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)



    # In[7]:


    #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    #https://splinter.readthedocs.io/en/latest/finding.html
    browser.find_by_id('full_image').click()
    time.sleep(3)
    browser.click_link_by_partial_text('more info')


    # In[8]:


    #find and parse new url
    new_jpl_html = browser.html
    new_image_soup = bs(new_jpl_html, 'html.parser')


    # In[9]:


    #Make sure to find the image url to the full size .jpg image.
    image_url = new_image_soup.find('img', class_='main_image')
    partial_url = image_url.get('src')


    # In[10]:


    #Make sure to save a complete url string for this image...and assign the url string to a variable called featured_image_url.
    featured_image_url = f'https://www.jpl.nasa.gov{partial_url}'
    time.sleep(1)
    print(featured_image_url)


    # # Mars Weather

    # In[11]:


    #Visit the Mars Weather twitter account 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    weather_url = "https://twitter.com/marswxreport"
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')


    # In[12]:


    #scrape the latest Mars weather tweet from the page. 
    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)


    # # Mars Facts

    # In[13]:


    #Visit the Mars Facts webpage 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)


    # In[14]:


    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_table = pd.DataFrame(pd.read_html(facts_url)[0])
    facts_table.head()


    # In[15]:


    #Use Pandas to convert the data to a HTML table string.
    mars_facts = facts_table.to_html(header = False, index = False)
    print(mars_facts)
    facts_table.to_html('mars_facts.html')


    # # Mars Hemispheres

    # In[16]:


    #Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
 



    # In[17]:


    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #hemi data container
    hemi_info = []
    #loop through, click, find and store url, title related to each hyperlinked hemisphere
    for hemi in range (4):
        time.sleep(3)
    #find hyperlink
        images = browser.find_by_tag('h3')
    #click hyperlink
        images[hemi].click()
    #read and find title and url
        hemi_loop = browser.html
        soup = bs(hemi_loop, "html.parser")
        img_title = soup.find('h2',class_='title')
        back_url = soup.find("img", class_="wide-image")["src"]
    #append url src to create full url
        img_url = f'https://astrogeology.usgs.gov{back_url}'
    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    #store loop list in hemi data container as a dictionary
        hemi_info.append({'title':img_title,'img_url':img_url})
        browser.back()
    #print hemi data container after loop
    pprint(hemi_info) 

    mars_data = {
        "Headline": news_title,
        "Desription": news_parag,
        "Featured_Image": featured_image_url,
        "Current_Weather": mars_weather,
        "Facts": mars_facts,
        "Hemis": hemi_info
        }

    return mars_data