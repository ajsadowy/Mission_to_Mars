#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt



def scrape_all():
    # Initiate headless driver for deployment
    
    browser = Browser('chrome', executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# Visit the NASA Mars News Site
def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### JPL Space Images Featured Image
# Visit URL
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ### Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL 
def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #items = browser.find_by_css('a.product-item h3')
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        
	# Create an empty dictionary
        # hemispheres = {}
        
        browser.find_by_css('a.product-item h3')[i].click()
        #element = browser.find_link_by_text('Sample').first
        #img_url = element['href']
        #title = browser.find_by_css("h2.title").text
        #hemispheres["img_url"] = img_url
        #hemispheres["title"] = title
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_image_urls.append(hemisphere_data)
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
   
    hemi_soup = soup(html_text, "html.parser")
    # Try/Except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
    except AttributeError:
        # Image error will return "None"
        title_elem = None
        sample_elem = None
    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }
    return hemispheres

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())