#Importing packages
from selenium import webdriver
import pandas as pd

# driver = webdriver.Chrome('')
driver= webdriver.Chrome()
# url = driver.get('https://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans/p702')
url = driver.get('https://www.justdial.com/Kolkata/gym')

print(url)