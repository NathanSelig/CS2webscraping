import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime



#region functions
def stock_information(page, stock_name):
    user_soup = BeautifulSoup(page.content, 'html.parser') 
    #region price of stock
    stock_price  = user_soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
    stock_info = user_soup.find('table', class_ = 'W(100%)')
    time_of_data = user_soup.find('div', id = 'quote-market-notice')
    
    stock_history(stock_name)

    print(stock_price['value'], '  ')
    print('')
    print(stock_info.get_text())
    print('')
    print(time_of_data.get_text())
    #endregion

def getDB():
    file = 'commonstocks.csv'
    database = pd.read_csv(file, index_col = 0)

def compare(input):
    starhill_variable = str(input).split()
    
def stock_history(stock_name):
    history_url = requests.get(f'https://finance.yahoo.com/quote/AMZN/history')
    history_soup = BeautifulSoup(history_url.content, 'html.parser')
    table = history_soup.find('table', class_ = 'W(100%) M(0)')
    table_data = table.find('tbody').find_all('tr')
    
#endregion

#* page format etfs https://finance.yahoo.com/quote/%5E[stock name]?p=%5E[stock name]
#* page format stocks /quote/[stock name]
#* page format currency
#* materials

#region main page
#* go to yahoo page
main_page = requests.get('https://finance.yahoo.com')
print(f'Status: \n{main_page.status_code}')
main_soup = BeautifulSoup(main_page.content, 'html.parser')
#endregion

time = datetime.datetime.now()
print(time)
print('')

#* ask user what stocks they want to look at
print('what are you looking for: \nstock\netf\n')
choice = input("")

match choice:
    case 'stock':
        user_stock = input(f'what {choice} would you like to look at: ').upper()
        user_page = requests.get(f'https://finance.yahoo.com/quote/{user_stock}')
        stock_information(user_page, user_stock)
    case 'etf':
        user_stock = input(f'what {choice} would you like to look at: ').upper()
        user_page = requests.get(f'https://finance.yahoo.com/quote/%5E{user_stock}?p=%5E{user_stock}')
        stock_information(user_page)
    case 'compare stocks':
        user_stock = input(f'what {choice} would you like to compare: ').upper()
        compare(user_stock)