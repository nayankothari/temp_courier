# import requests

# url = "https://order-tracking.p.rapidapi.com/carriers"

# headers = {
# 	"Content-Type": "application/json",
# 	"X-RapidAPI-Key": "7e4a49d144mshbc654753cabfcb9p191f52jsnbaa54ce5a454",
# 	"X-RapidAPI-Host": "order-tracking.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

import requests

url = "https://trackcourier.io/api/v1/get_checkpoints_table/e8bb853c9121b286ae16987bcb997ff9/tirupati-courier/241100164222"
response = requests.post(url, headers={"content-type": "application/json"})
print(response.text)