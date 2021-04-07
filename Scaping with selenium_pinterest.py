#!/usr/bin/env python
# coding: utf-8

# In[1]:


# need to install these first, and also download webdriver(chrome)
# pip install selenium
# pip install webdriver_manager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


# In[2]:


#instantiate the Chrome class web driver and pass the Chrome Driver Manager
driver = webdriver.Chrome(ChromeDriverManager().install())

#Maximize the Chrome window to full-screen
driver.maximize_window() 


# In[3]:


#go to Pinterest's Login page
driver.get("https://www.pinterest.com/login/")


# In[4]:


# login to account before starting to scrape
# email
driver.find_element_by_xpath('//*[@id="email"]').send_keys('pewaw63939@684hh.com')

# password
driver.find_element_by_xpath('//*[@id="password"]').send_keys('datafocusedpythoN')

# click login button
driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()


# In[6]:


# scrape data!
#driver.get("https://www.pinterest.com/")

images = []

# get five scrolls of data
for _ in range(1,5):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    # get the image from div with pinrep-image test-id
    for img in soup.find_all('div', {"data-test-id":"pinrep-image"}):
        target = img.find('img')
        if target is not None:
            #print(target.get('src'))
            str = target.get('src')
            images.append(f'{str}\n')
    
    # scroll down
    driver.execute_script("window.scrollTo(1,100000)")
    print("scrolling")
    time.sleep(1)

print(images)


# In[7]:


# write to file
with open ('pinterest_img.txt', 'w', encoding = 'utf-8') as pin_img:
    pin_img.writelines(lines for lines in images)


# In[8]:


driver.quit()

