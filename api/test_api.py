# import requests

# url = "https://order-tracking.p.rapidapi.com/carriers"

# headers = {
# 	"Content-Type": "application/json",
# 	"X-RapidAPI-Key": "7e4a49d144mshbc654753cabfcb9p191f52jsnbaa54ce5a454",
# 	"X-RapidAPI-Host": "order-tracking.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)


test_data = {
    "Tirupati": "https://trackcourier.io/api/v1/get_checkpoints_table/e8bb853c9121b286ae16987bcb997ff9/tirupati-courier/",
    "ST courier": "https://trackcourier.io/api/v1/get_checkpoints_table/e8bb853c9121b286ae16987bcb997ff9/st-courier/",
    "Professional": "https://trackcourier.io/api/v1/get_checkpoints_table/e8bb853c9121b286ae16987bcb997ff9/professional-courier/",
}


# import requests
# import time


# https://www.tracktry.com/index_ajax.php?tracknumber=392227081439&lang=en
# #                                                                                        1672941390818
# url = "https://www.tracktry.com/track/241100164235/shree-tirupati"
# response = requests.get(url)
# # , headers={"content-type": "application/json"})
# print(response.text)

import requests
from bs4 import BeautifulSoup

url = "https://www.tracktry.com/track/241100164235/shree-tirupati"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
class_ = "Tracking-result"
lists = soup.find_all("div", class_="Tracking-result")
print(lists)




