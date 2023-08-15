# import requests

# url = "https://order-tracking.p.rapidapi.com/carriers"

# headers = {
# 	"Content-Type": "application/json",
# 	"X-RapidAPI-Key": "7e4a49d144mshbc654753cabfcb9p191f52jsnbaa54ce5a454",
# 	"X-RapidAPI-Host": "order-tracking.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)


# test_data = {
#     "Tirupati": "https://trackcourier.io/api/v1/get_checkpoints_table/cd134aa029084eb33f8ea379f30a3df0/tirupati-courier/",
#     "ST courier": "https://trackcourier.io/api/v1/get_checkpoints_table/e8bb853c9121b286ae16987bcb997ff9/st-courier/",
#     "Professional": "https://trackcourier.io/api/v1/get_checkpoints_table/e8bb853c9121b286ae16987bcb997ff9/professional-courier/",
# }


# import requests
# import time


# url = "https://pushpakcourier.net/query.php"
# res = requests.post(url=url, headers={"content-type": "application/json"}, data={"trackcode": 151874420, "IDType": "Doc_No"})
# print(res.text)


# https://www.tracktry.com/index_ajax.php?tracknumber=392227081439&lang=en
# #                                                                                        1672941390818
# url = "https://www.tracktry.com/track/241100164235/shree-tirupati"
# response = requests.get(url)
# # , headers={"content-type": "application/json"})
# print(response.text)

# import requests
# from bs4 import BeautifulSoup

# url = "https://www.tracktry.com/track/241100164235/shree-tirupati"
# response = requests.get(url)

# soup = BeautifulSoup(response.content, 'html.parser')
# class_ = "Tracking-result"
# lists = soup.find_all("div", class_="Tracking-result")
# print(lists)

import time
import warnings
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


warnings.filterwarnings("ignore")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.binary_location = "/usr/local/bin/chromedriver"
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")

def get_search_details(*args, **kwargs):        
    if str(kwargs.get("courier")).__contains__("madhur"):
        try:
            # driver = webdriver.Chrome('D:\Python django folder\Temp_courier\courier\api\chromium_driver\\', chrome_options=chrome_options)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.switch_to.new_window('tab')
            driver.get("https://www.madhurcouriers.in/CNoteTracking")
            search_bar = driver.find_element("id", "ContentPlaceHolder1_txtCNote")
            search_bar.clear()
            search_bar.send_keys(kwargs.get("doc_number"))
            search_bar.send_keys(Keys.RETURN)
            element_present = EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_gvBookings'))
            WebDriverWait(driver, 5).until(element_present)
            data = pd.read_html(driver.find_element("xpath","//table[@id='ContentPlaceHolder1_gvBookings']").get_attribute('outerHTML'))[0]
            driver.close()            
            final_list = []
            for i in data.values:
                final_data = {}
                final_data["Date"] = i[1]
                final_data["Location"] = ""
                final_data["Activity"] = i[2]
                final_data["CheckpointState"] = i[3]
                final_list.append(final_data)
            return final_list
        except Exception as e:
            print(e)
            return [{}]
        
    elif str(kwargs.get("courier")).__contains__("goodluck"):
        try:
            # driver = webdriver.Chrome('D:\Python django folder\Temp_courier\courier\api\chromium_driver\\', chrome_options=chrome_options)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.switch_to.new_window('tab')            
            driver.get("http://94.130.15.229/goodluck/onlinetracking.aspx")
            search_bar = driver.find_element("id", "txtcnote")
            search_bar.clear()
            search_bar.send_keys(kwargs.get("doc_number")) 
            l = driver.find_element("xpath", "//input[@class='btn_act']")
            l.click()
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'table'))
            WebDriverWait(driver, 5).until(element_present)                        
            data = driver.find_elements("xpath","//table[@rules='all']")
            final_list = []            
            for j in data:                 
                new_df = pd.read_html(j.get_attribute("outerHTML"))
                new_df = pd.concat(new_df)                
                for i in new_df.values:
                    final_data = {}
                    final_data["Date"] = i[1]
                    final_data["Location"] = ""
                    final_data["Activity"] = i[2]
                    try:
                        final_data["CheckpointState"] = i[5]
                    except:
                        final_data["CheckpointState"] = i[4]
                    final_list.append(final_data)
            driver.close()  
            return final_list
        except Exception as e:
            print(e)
            return [{}]
    elif str(kwargs.get("courier")).__contains__("pushpak"):
        url = "https://www.pushpakcourier.net/query.php"
        try:
            # driver = webdriver.Chrome('D:\Python django folder\Temp_courier\courier\api\chromium_driver\\', chrome_options=chrome_options)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.switch_to.new_window('tab')
            driver.get(url)
            search_bar = driver.find_element("name", "trackcode")
            search_bar.clear()
            search_bar.send_keys(kwargs.get("doc_number"))
            search_bar.send_keys(Keys.RETURN)
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'CSSTableGenerator'))
            WebDriverWait(driver, 5).until(element_present)
            data = driver.find_elements("xpath","//table[@border='1']") #.get_attribute('outerHTML'))[0]
            if len(data) >= 2:                
                for i in data:
                    new_df = pd.read_html(i.get_attribute("outerHTML"))
                    new_df = pd.concat(new_df)                                                
                final_list = []
                for i in new_df.values:                    
                    final_data = {}
                    final_data["Date"] = i[0]
                    final_data["Location"] = ""
                    final_data["Activity"] = i[1]
                    final_data["CheckpointState"] = i[2]
                    final_list.append(final_data)
            driver.close()                        
            return final_list
        except Exception as e:
            print(e)
            return [{}]


# data = get_search_details(courier="madhur", doc_number="p304416565")
# data = get_search_details(courier="goodluck", doc_number="15149233")
# data = get_search_details(courier="pushpak", doc_number="1234")
# print(data)
