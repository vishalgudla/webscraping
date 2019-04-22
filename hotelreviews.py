from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import random

hotel_ff = pd.DataFrame(pd.read_csv("Frankfurt hotel links.csv"))
links = hotel_ff.hotel_link
numbers= random.sample(range(1,len(hotel_ff.hotel_link)),80)
numbers.sort()
k=0

d = {'hotel_name': [],'name': [], 'overall_rating': [],'overall_review': [],'location_and_surrounding_review': [],'location_and_surrounding_rating': [],
    'room_review': [],'room_rating': [],'service_review': [], 'service_rating': [], 'gastronomy_review': [],'gastronomy_rating': [],
    'sports_and_entertainment_review': [],'sports_and_entertainment_rating': [],'hotel_review': [],
     'hotel_rating': [],'traveled_as':[],'children':[],'duration':[],'reason_for_travel':[],'age_group':[],'reviews_written':[]}

review_df = pd.DataFrame(data=d)


hotel = len(hotel_ff.name)

              # i refers to total no. of hotels
i=1
while i<= len(numbers):
    scrapelink = links[numbers[i]]
    wd = webdriver.Firefox()
    wd.get(scrapelink)
    
    # Wait for the dynamically loaded elements to show up
    WebDriverWait(wd, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "navigation-bar-item-content")))

    # And grab the page HTML source
    html_page = wd.page_source
    wd.quit()

    soup = BeautifulSoup(html_page,"html.parser")
    
    for max_page in soup.find_all('a', {'class': 'navigation-bar-item-content'}):
        reviews_link = max_page['href']
        
        if reviews_link.find("bewertungen"):
            
            reviews_link = "https://www.holidaycheck.de" + reviews_link
            
            break
    
    
    #print(reviews_link)
    
    
    #grab the HTML page source for reveiws page of each hotel
    wd = webdriver.Firefox()
    wd.get(reviews_link)
    
    WebDriverWait(wd,10).until(
    EC.visibility_of_element_located((By.CLASS_NAME,'text-and-link-container')))
    
    html_page= wd.page_source
    wd.quit()
    
    soup = BeautifulSoup(html_page,"html.parser")
    
    #get total no. of reviews
    
    for h2text in soup.find_all('h2',{'class':'hotelReview-list-headline'}):
        numbers_rev = h2text.text.split()
        number_reviews=int(numbers_rev[0])
        #print(number_reviews)  --------- Prints the total no. of reviews
        
    for review_page in soup.find_all('div',{'class':'text-and-link-container row'}):
        link_get = review_page.find('a')
        reviews_individual_link = "https://www.holidaycheck.de"+link_get['href']
        #print(reviews_individual_link)   -------- Prints the link to individual reviews  
        break
    
    j=0  # j keeps a count of total reviews to be scrapped for a particular hotel
    
    while j<=number_reviews:
        
        wd = webdriver.Firefox()
        wd.get(reviews_individual_link)




        content = wd.find_element_by_class_name('hotelReviewHeader-firstName')
        review_df.ix[k,'hotel_name'] = hotel_ff['name'].iloc[numbers[i]]
        review_df.ix[k,'name'] = content.text
       
        

        average_text_rating = wd.find_element_by_class_name('average-text-rating')
        average_rating_overall = average_text_rating.text.split('/')
        print(average_rating_overall[0])
        
        review_df.ix[k,'overall_rating'] = float(average_rating_overall[0].replace(',','.'))
       

        general_comment = wd.find_element_by_class_name('general-content')
        review_df.ix[k,'overall_review'] = general_comment.text
        

        group_label_list = []
        average_rating_element = wd.find_elements_by_class_name('aspect-group-label')
        for y in average_rating_element:
            group_label_list.append(y.text)
        print(group_label_list)
        
        individual_rating_list = []
        average_rating = wd.find_elements_by_class_name('average-rating')
        for x in average_rating:
            individual_rating_list.append(float(x.text.replace(',','.')))
        print(individual_rating_list)
        
        individual_review_list = []
        text_reviews = wd.find_elements_by_class_name('text-reviews')
        for m in text_reviews:
            individual_review_list.append(m.text)
        print(individual_review_list)
        
        if len(individual_review_list) != 0:
            for x,y,z in zip(group_label_list,individual_review_list,individual_rating_list):
                if x == "Lage & Umgebung":
                    review_df.ix[k,'location_and_surrounding_review'] = y
                    review_df.ix[k,'location_and_surrounding_rating'] = z
                elif x == "Zimmer":
                    review_df.ix[k,'room_review'] = y
                    review_df.ix[k,'room_rating'] = z
                elif x == "Service":
                    review_df.ix[k,'service_review'] = y
                    review_df.ix[k,'service_rating'] = z
                elif x == "Gastronomie":
                    review_df.ix[k,'gastronomy_review'] = y
                    review_df.ix[k,'gastronomy_rating'] = z
                elif x == "Sport & Unterhaltung":
                    review_df.ix[k,'sports_and_entertainment_review'] = y
                    review_df.ix[k,'sports_and_entertainment_rating'] = z
                else:
                    review_df.ix[k,'hotel_review'] = y
                    review_df.ix[k,'hotel_rating'] = z
        else:
            for x,z in zip(group_label_list,individual_rating_list):
                if x == "Lage & Umgebung":
                    
                    review_df.ix[k,'location_and_surrounding_rating'] = z
                elif x == "Zimmer":
                    
                    review_df.ix[k,'room_rating'] = z
                elif x == "Service":
                
                    review_df.ix[k,'service_rating'] = z
                elif x == "Gastronomie":
                    
                    review_df.ix[k,'gastronomy_rating'] = z
                elif x == "Sport & Unterhaltung":
                   
                    review_df.ix[k,'sports_and_entertainment_rating'] = z
                else:
                    
                    review_df.ix[k,'hotel_rating'] = z
        
        #collecting information about trip and reviewer
        info_about_trip = []
        info_about_reviewer = []
        information = []
        
        additional_info = wd.find_elements_by_tag_name('tr')
        for d in additional_info:
            information.append(d.text)
        info_about_trip = information[1:information.index("Infos zum Bewerter")]
        info_about_reviewer = information[information.index("Infos zum Bewerter")+1:]
        print(info_about_trip)
        print(info_about_reviewer)
        
      
        
        
        for a in info_about_trip:
            a_new = a.split(': ')
            if a_new[0] == "Verreist als":
                review_df.ix[k,'traveled_as'] = a_new[1]
            elif a_new[0] == "Kinder":
                review_df.ix[k,'children'] = a_new[1]
            elif a_new[0] == "Dauer":
                review_df.ix[k,'duration'] = a_new[1]
            else:
                review_df.ix[k,"reason_for_travel"] = a_new[1]
                
        for b in info_about_reviewer:
            b_new = b.split(': ')
            if b_new[0] == "Alter":
                review_df.ix[k,'age_group'] = b_new[1]
            elif b_new[0] == "Bewertungen":
                review_df.ix[k,'reviews_written'] = b_new[1]
            
        
        
        review_df.to_csv('information.csv')
        if j != number_reviews-1:
            checklist = wd.find_elements_by_class_name("next")
            if len(checklist) !=0:
                WebDriverWait(wd,10).until(
                EC.visibility_of_element_located((By.CLASS_NAME,'next')))

                html_page= wd.page_source
                wd.quit()
                soup = BeautifulSoup(html_page,"html.parser")
                for next_page in soup.find_all('div',{'class':'next'}):
                    link_get = next_page.find('a')

                    next_page_link = "https://www.holidaycheck.de"+link_get['href']
                    print(next_page_link)
                    break
                reviews_individual_link = next_page_link
            else:
                wd.quit()
        else:
            wd.quit()
        
        k=k+1
        j=j+1
    i=i+1

    
    #Open the first review html page on new browser
    
	
    
    
    
    
    
    
