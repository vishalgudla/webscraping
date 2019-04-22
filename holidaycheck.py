from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

num=1

scrapelink = "https://www.holidaycheck.de/dh/hotels-frankfurt-am-main/0df2e7c6-0ff8-332b-8455-6ff92921ee4b?adults=2&departuredate=2019-03-10&duration=exactly&numberOfRooms=1&p="+ str(num) +"&returndate=2019-03-11&travelkind=hotelonly"
wd = webdriver.Chrome()
wd.get(scrapelink)

# Wait for the dynamically loaded elements to show up
WebDriverWait(wd, 10).until(
   	EC.visibility_of_element_located((By.CLASS_NAME, "hotel-title-link")))

# And grab the page HTML source
html_page = wd.page_source
wd.quit()

soup = BeautifulSoup(html_page,"html.parser")

for max_page in soup.find_all('div', {'class': 'max-page'}):
    number_list = max_page.text.split()
max_page = int(number_list[1])



link_list = []
name_hotel = []
while num <= max_page :
	scrapelink = "https://www.holidaycheck.de/dh/hotels-frankfurt-am-main/0df2e7c6-0ff8-332b-8455-6ff92921ee4b?adults=2&departuredate=2019-03-10&duration=exactly&numberOfRooms=1&p="+ str(num) +"&returndate=2019-03-11&travelkind=hotelonly"

# Start the WebDriver and load the page
	wd = webdriver.Chrome()
	wd.get(scrapelink)

# Wait for the dynamically loaded elements to show up
	WebDriverWait(wd, 10).until(
    	EC.visibility_of_element_located((By.CLASS_NAME, "hotel-title-link")))

# And grab the page HTML source
	html_page = wd.page_source
	wd.quit()

	soup = BeautifulSoup(html_page,"html.parser")

	
	for link in soup.find_all("a", {"class": "hotel-title-link"}):
	    link_list.append("https://www.holidaycheck.de/"+link.get('href'))
	#    print(link.get('href'))
	print(link_list)
	for text in soup.find_all("h3",{"class":"hotel-title-with-stars"}):
	    name_hotel.append(text.text)
	#    print(text.text)
	print(name_hotel)   

	num = num + 1

	

df = pd.DataFrame({"Hotel Name":name_hotel,
	                  "Hotel Link":link_list})

print(df)
df.to_csv("output.csv", index=False)