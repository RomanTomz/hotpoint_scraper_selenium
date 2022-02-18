#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# todo: add url from base url + href


# In[50]:


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import numpy as np


from time import sleep

# from bs4 import BeautifulSoup


# In[59]:


driver = webdriver.Chrome(executable_path='/Users/admin/.wdm/drivers/chromedriver/mac64/98.0.4758.80/chromedriver')
models = ['DD2540BL','SI4 854 P IX','SA2540HIX','FA4S541JBLGH','FA4S544IXH']
parts = ['Electrics','Heating Elements']

names_list = []
avail_list = []
price_list = []
models_list = []
part_type = []

driver.get("https://parts.hotpoint.co.uk")
driver.implicitly_wait(10)

# Tell cookies to fuck off
driver.find_element(By.XPATH,"//div[@class='banner-actions-container']/button[@id='onetrust-accept-btn-handler']").click()
sleep(1)

for model in models:
    # Initialise driver on page
    
    driver.get("https://parts.hotpoint.co.uk")
    
    # scroll to searchbar
    element = driver.find_element(By.XPATH, "//div[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete__wrapper']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    sleep(0.5)
    
    # click on searchbar and enter model number
    driver.find_element(By.XPATH,"//div[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete__wrapper']/input[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete__input']").click()
    driver.find_element(By.XPATH,"//div[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete__wrapper']/input[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete__input']").send_keys(model)
    sleep(1)
    try:
        driver.find_element(By.XPATH,"//div[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete__results']/a/div").click() # if model on dropdown, click
        sleep(1)
    except NoSuchElementException:
        driver.find_element(By.XPATH,"//div[@class='smartukb2c-custom-autocomplete-2-x-customAutocomplete']/a").click() # if model not on dropdown click on lens and then click on diagram
        sleep(1)
        driver.find_element(By.XPATH,"//div[@class='vtex-product-summary-2-x-productNameContainer mv0 vtex-product-summary-2-x-nameWrapper overflow-hidden c-on-base f5']").click()
    
    
    
    for part in parts:    
        driver.find_element(By.XPATH,f"//div[@data-name='{part}']").click()

        # page_source = driver.page_source
        
        spares = driver.find_elements(By.XPATH,"//div[@class='smartukb2c-custom-product-page-0-x-customProductPageSparePartsCard']") # grab root div for product grid
        for spare in spares:
            name = spare.find_element(By.XPATH,".//div[@class='smartukb2c-custom-product-page-0-x-customProductPageSparePartsCardInfo']/a").text
            availability = spare.find_element(By.XPATH,".//div[@class='smartukb2c-custom-product-page-0-x-availabilityDiv']").text
            try:
                price = spare.find_element(By.XPATH,".//div[@class='smartukb2c-custom-product-page-0-x-customProductPageSparePartsCardFooter']/span/span/span/span[2]").text
            except NoSuchElementException:
                price = ''
            model = model
            part_cat = part
            # print(name,availability,price,model)
            names_list.append(name)
            avail_list.append(availability)
            price_list.append(price)
            models_list.append(model)
            part_type.append(part_cat)
            
df = pd.DataFrame(np.column_stack([names_list, avail_list, price_list, models_list, part_type]), 
                               columns=['name', 'availability', 'price', 'model','part_type'])           

driver.quit()


# In[60]:


df


# In[53]:


# spares = driver.find_elements_by_xpath("//div[@class='smartukb2c-custom-product-page-0-x-customProductPageSparePartsCard']")
# for spare in spares:
#     name = spare.find_element_by_xpath(".//div[@class='smartukb2c-custom-product-page-0-x-customProductPageSparePartsCardInfo']/a").text
#     availability = spare.find_element_by_xpath(".//div[@class='smartukb2c-custom-product-page-0-x-availabilityDiv']").text
#     print(name,availability)


# In[ ]:




