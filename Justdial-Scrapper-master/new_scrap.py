
#import neccasary libraries
from bs4 import BeautifulSoup
import requests
import csv
# import urllib2
import time
from selenium import webdriver

browser = webdriver.Chrome()

def get_soup(link):
    browser.get(link)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = browser.page_source
    soup = BeautifulSoup(html)
    return soup
    

def get_name(petshop):
    return petshop.find('span', {'class':'lng_cont_name'}).string


def get_address(body):
    return body.find('span', {'class':'mrehover'}).text.strip()


def which_digit(html):
    mappingDict={'icon-ji':9,
                'icon-lk':8,
                'icon-nm':7,
                'icon-po':6,
                'icon-rq':5,
                'icon-ts':4,
                'icon-vu':3,
                'icon-wx':2,
                'icon-yz':1,
                'icon-acb':0,
                }
    return mappingDict.get(html,'')

def get_phone_number(body):
    i=0
    for item in body.find('p',{'class':'contact-info'}):
        i+=1
        if(i==2):
            phoneNo=''
            try:
                for element in item.find_all(class_=True):
                    classes = []
                    classes.extend(element["class"])
                    phoneNo+=str((which_digit(classes[1])))
            except:
                pass
            return phoneNo

CityList=['']#Enter The list of cities here


fields = ['Name', 'Address','Phone Number']


urlSkeleton1="https://www.justdial.com/"
urlSkeleton2="/Pet-Grooming-Services/nct-11002277/page-"#Sample search url. Keep up with this format when you choose your links
for city in CityList:
    page_number = 1
    out_file = open((str(city)+'.csv'),'wb')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

    # Write fields first
    csvwriter.writerow(dict((fn,fn) for fn in fields))

    while page_number < 60:#From page 61, we get into a loop. Some items may not need all 60 pages, choose wisely to save time.
        link=urlSkeleton1+str(city)+urlSkeleton2+str(page_number)
        
        soup = get_soup(link, "lxml")
    
        services = soup.find_all('li', {'class': 'cntanr'})
    
        for petshop in services:
            petStore={}
            petStore['Name'] = get_name(petshop)
            petStore['Address']=get_address(petshop)
            try:
                petStore['Phone Number']=get_phone_number(petshop)
            except:
                petStore['Phone Number']='None'#Some places were found not to have numbers
            csvwriter.writerow(petStore)
        
        page_number += 1
    
        time.sleep(5)
    # print city,"is over"
    out_file.close()