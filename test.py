import requests

URL = 'https://finance.yahoo.com/quote/AMZN/history?p=AMZN'

response = requests.get(URL)

open('data.csv', 'wb').write(response.content)




