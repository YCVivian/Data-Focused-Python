#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

# Install the selenium package first, and also download webdriver(chrome)
# pip install selenium
# pip install webdriver_manager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd


"""
Log into Pinterest before getting data from the website
"""
# dummy account for testing purposes
USER_EMAIL = 'pewaw63939@684hh.com'
USER_PASSWORD = 'datafocusedpythoN'

#instantiate the Chrome class web driver and pass the Chrome Driver Manager
driver = webdriver.Chrome(ChromeDriverManager().install())

#Maximize the Chrome window to full-screen
driver.maximize_window() 

#go to Pinterest's Login page
driver.get("https://www.pinterest.com/login/")

# locate and enter email
driver.find_element_by_xpath('//*[@id="email"]').send_keys(USER_EMAIL)

# locate and enter password
driver.find_element_by_xpath('//*[@id="password"]').send_keys(USER_PASSWORD)

# click login button to submit
driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()




"""
Scrape data from the website
pick up at least 5 pages of data

"""
data = []

# get five scrolls of data
for _ in range(1,5):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    # locate each post
    for post in soup.find_all('div', {"data-test-id":"pinWrapper"}):
        
        # locate the image of the post
        target = post.find('div', {"data-test-id":"pinrep-image"})
        #locate the author of the post
        target2 = post.find('div', {"data-test-id":"pointer-events-wrapper"})
        
        if target is not None:
            post_data = []
            
            # Image
            if target.find('img') is not None:
                image_url = target.find('img').get('src')
                post_data.append(image_url)
            
            # Author
            if target2 is not None:
                author_tag = target2.find('a')
                if author_tag is not None:
                    author = author_tag.find('div', {'class': 'tBJ dyH iFc MF7 pBj DrD IZT swG z-6'})
                    if author is not None:
                        post_data.append(author.text)
            
            data.append(post_data)
                

    
    # scroll down
    driver.execute_script("window.scrollTo(1,100000)")
    print("scrolling")
    time.sleep(1)

# print(data)



# write to file (raw data)
with open ('pinterest_raw.csv', 'w', encoding = 'utf-8') as pin_img:
    for d in data:
        for i in d:
            pin_img.writelines(i+'\n')


# format (clean data)
df = pd.DataFrame(data, columns=['pin_url', 'author'])
df['user'] = USER_EMAIL
df['id'] = df.index
df['category'] = 'pinterest'
df.head()


# store clean data
df.to_csv('pinterest_cleaned.csv', index=False)


# close the driver
driver.quit()
