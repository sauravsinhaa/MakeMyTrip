# Script for scraping hotel data of any given city!
# Data scraping is taking place through chromedriver(replace chromedriver.exe file if outdated). Chrome browser should be available in your system.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from json import dumps 
import pandas as pd 
import time
import csv
chrome_browser_path = r"C:\Users\saura\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
service = Service(chrome_browser_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("enable-automation")
# chrome_options.add_argument("--window-size=700,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("enable-features=NetworkServiceInProcess")
chrome_options.add_argument("disable-features=NetworkService")
chrome_options.add_argument("--start-maximized")
prefs = {"profile.managed_default_content_settings.images": 1}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=service,options=chrome_options)

# Add the browser url below after selecting city and dates.
# example link: https://www.makemytrip.com/hotels/hotel-listing/?checkin=08212023&city=CTCCU&checkout=08222023&roomStayQualifier=2e0e&locusId=CTCCU&country=IN&locusType=city&searchText=Kolkata&regionNearByExp=3&rsc=1e2e0e

MMT_LINK = "https://www.makemytrip.com/hotels/hotel-listing/?checkin=05302024&checkout=05312024&locusId=CTCCU&locusType=city&city=CTCCU&country=IN&searchText=Kolkata&roomStayQualifier=2e0e&_uCurrency=INR&reference=hotel&type=city&rsc=1e2e0e" 

CSV_PATH =r"C:\Users\saura\Downloads\JeddhaMarkeyu.csv"

driver.get(MMT_LINK)
time.sleep(20)
print("6 sec over")



for i in range(0,101):
    print("hotel: "+str(i))
    content = driver.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]')
    hname = content.find_element(By.ID,'hlistpg_hotel_name')
    print(hname.text)
    try:
        rating = content.find_element(By.ID,'hlistpg_hotel_user_rating')
        rating = rating.text
        print(rating)
        try:
            rating_desc = content.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]/a/div/div[1]/div[2]/div[1]/div/div/span[1]')
            rating_desc = rating_desc.text
            print(rating_desc)
        except:
            rating_desc = content.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]/a/div/div/div[1]/div[2]/div[2]/div/div/span[2]')
            rating_desc = rating_desc.text
            print(rating_desc.text)
        review_count = content.find_element(By.ID,'hlistpg_hotel_reviews_count')
        review_count = review_count.text
        print(review_count)
    except:
        rating=""
        rating_desc=""
        review_count=""
    
    loc = content.find_element(By.CLASS_NAME,'pc__html')
    loc = loc.text
    loc = loc.split("|")
    location = loc[0] #hotel_locationzdb
    try:
        landmark = loc[1].split('from')
        dist_landmark = landmark[0].lstrip() 
        landmark = landmark[1].lstrip() #nearest landmark/locality
    except:
        dist_landmark=""
        landmark=""

    print("location: "+location)
    print("landmark: "+landmark)
    print("dis to landmark: "+dist_landmark)
    
  
    price = content.find_element(By.ID,'hlistpg_hotel_shown_price')
    print(price.text[2:])
    
    
    try:
        tax = content.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]/a/div[1]/div/div[2]/div/div/p[2]')
        tax = tax.text.split(" ")[2]
    except:
        tax=""
    print(tax)
    
    try:
        s_rating = content.find_element(By.ID,'hlistpg_hotel_star_rating')
        s_rating = s_rating.get_attribute('data-content')
    except:
        s_rating=""
    
    print("s_rating: "+s_rating) #star_rating
    
    #csv
    data=[[hname.text,rating,rating_desc,review_count,s_rating,location,landmark,dist_landmark,price.text[2:],tax]]
    with open(CSV_PATH,'a',newline='') as file:
                writer=csv.writer(file)
                writer.writerows(data)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

driver.close()
