from __future__ import print_function

import re
import time

from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver.common.by import By

# generate query url for search terms
def google_gen_query_url(keywords):
    base_url = "https://www.google.com/search?tbm=isch&hl=en"
    keywords_str = "&q=" + quote(keywords) # queried phrase
    query_url = base_url + keywords_str
    # disable safe search to get more images
    query_url += "&safe=off"

    return query_url

# get all image urls from a image search
def google_image_url_from_webpage(driver, max_number):
    thumb_elements_old = []
    thumb_elements = []
    while True:
        try:
            thumb_elements = driver.find_elements(By.CLASS_NAME, "rg_i")
            print("Found {} images.".format(len(thumb_elements)))
            if len(thumb_elements) >= max_number:
                break # found enough images, exit
            if len(thumb_elements) == len(thumb_elements_old):
                break # found no more new images, exit
            thumb_elements_old = thumb_elements
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to find more images
            time.sleep(3) # to give time for scrolling
            show_more = driver.find_elements(By.CLASS_NAME, "mye4qd")
            if len(show_more) == 1 and show_more[0].is_displayed() and show_more[0].is_enabled():
                show_more[0].click() # show more images on webpage
            time.sleep(2) # to avoid being blacklisted
        except Exception as e:
            print("Exception ", e)
            pass
    
    if len(thumb_elements) == 0:
        return [] # found no pictures

    print("Clicking on each thumbnail image ...")

    for i, elem in enumerate(thumb_elements):
        try:
            if i != 0 and i % 50 == 0:
                print(f"{i} thumbnail clicked.")
            if not elem.is_displayed() or not elem.is_enabled():
                continue
            elem.click()
        except Exception as e:
            print("Error while clicking in thumbnail:", e)
    
    image_elements = driver.find_elements(By.CLASS_NAME, "islib")
    image_urls = []
    url_pattern = r"imgurl=\S*&amp;imgrefurl"

    for image_element in image_elements[:max_number]:
        outer_html = image_element.get_attribute("outerHTML")
        re_group = re.search(url_pattern, outer_html)
        if re_group is not None:
            image_url = unquote(re_group.group()[7:-14])
            image_urls.append(image_url)
    return image_urls

# get image urls using a search word
def crawl_image_urls(keywords, max_number=1500):
    print("\nScraping From Google Images ...\n")
    print("Keyword: "+keywords)
    print("Number of image: ",max_number)
    # generate query to search for google
    query_url = google_gen_query_url(keywords)

    print("Query URL:  " + query_url)

    image_urls = []

    chrome_path = "./chromedriver.exe" # from https://chromedriver.chromium.org/downloads
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless") # don't show annoying popup windows
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    driver.get(query_url)
    # get image urls
    image_urls = google_image_url_from_webpage(driver, max_number)
    driver.close()
    outputcnt = len(image_urls)
    if len(image_urls) > max_number:
        outputcnt = max_number
    print("\n {0} valid crawled images urls will be used.\n".format(outputcnt))

    return image_urls[0:outputcnt]
