from bs4 import BeautifulSoup
# import urllib
import urllib.request
import csv
from selenium import webdriver
import pandas as pd

def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return body.find('span', {'class':'jcn'}).a.string

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

# def get_phone_number(body):
# 	try:
# 		return body.find('p', {'class':'contact-info'}).span.a.string
# 	except AttributeError:
# 		return ''

def get_phone_number(body):
	i=0
	if body.find('p',{'class':'contact-info'}):
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

def get_rating(body):
	rating = 0.0
	text = body.find('span', {'class':'star_m'})
	if text is not None:
		for item in text:
			rating += float(item['class'][0][1:])/10

	return rating

def get_rating_count(body):
	text = body.find('span', {'class':'rt_count'}).string

	# Get only digits
	rating_count =''.join(i for i in text if i.isdigit())
	return rating_count

def get_address(body):
	return body.find('span', {'class':'mrehover'}).text.strip()

def get_location(body):
	text = body.find('a', {'class':'rsmap'})
	if text == None:
		return
	text_list = text['onclick'].split(",")
	
	latitutde = text_list[3].strip().replace("'", "")
	longitude = text_list[4].strip().replace("'", "")
	
	return latitutde + ", " + longitude

n=10
for i in range(1,n+1):
	page_number = 1
	service_count = 1


	fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location']
	out_file = open('Delhi_Aluminium wholeseller-wholeseller_data'+str(i)+'.csv','w')
	csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

	# Write fields first
	csvwriter.writerow(dict((fn,fn) for fn in fields))

	while True:

		# Check if reached end of result
		if page_number > 1:
			break
		driver= webdriver.Chrome()
		# driver.get('https://www.justdial.com/Kolkata/gym')
		# driver.get('https://www.justdial.com/Mumbai/Aluminium-Foil-Wholesalers/nct-10014788')

		driver.get('https://www.justdial.com/Delhi/Aluminium-Foil-Wholesalers/nct-10014788/page-'+str(i))
		url = driver.page_source
		print(url)


		soup = BeautifulSoup(url, "html.parser")
		services = soup.find_all('li', {'class': 'cntanr'})


		# Iterate through the 10 results in the page
		for service_html in services:

			# Parse HTML to fetch data
			dict_service = {}
			name = get_name(service_html)
			phone = get_phone_number(service_html)
			rating = get_rating(service_html)
			count = get_rating_count(service_html)
			address = get_address(service_html)
			location = get_location(service_html)
			if name != None:
				dict_service['Name'] = name
			if phone != None:
				print('getting phone number')
				dict_service['Phone'] = phone
			if rating != None:
				dict_service['Rating'] = rating
			if count != None:
				dict_service['Rating Count'] = count
			if address != None:
				dict_service['Address'] = address
			if location != None:
				dict_service['Address'] = location

			# Write row to CSV
			csvwriter.writerow(dict_service)

			print("#" + str(service_count) + " " , dict_service)
			service_count += 1

		page_number += 1

	out_file.close()








