import requests
from bs4 import BeautifulSoup
import pandas as pd



#TODO take list of top 100 etf and stocks add to txt file \
#websites 
#https://stonks.news/top-100/robinhood
#turn into csv data



page = requests.get('https://stonks.news/top-100/robinhood')
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')

top100_table = soup.find('tbody', class_ = 'ant-table-tbody') 
top100 = top100_table.find_all('tr')


row = [i.find_all('td') for i in top100]
number = [i['data-row-key'] for i in top100]
name = [i[2].get_text() for i in row]
symbol = [i[1].get_text() for i in row]

table = pd.DataFrame({
    'rank':number,
    'name':name,
    'symbol':symbol,
})
file = 'commonstocks.csv'
table.to_csv(file, index=False)






