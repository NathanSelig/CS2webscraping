import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os


#region functions
def stock_information(page, stock_name):

    user_soup = BeautifulSoup(page.content, 'html.parser') 
    #region price of stock
    stock_price  = user_soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
    stock_info = user_soup.find('table', class_ = 'W(100%)')
    time_of_data = user_soup.find('div', id = 'quote-market-notice')
    

    print(stock_price['value'], '  ')
    print('')
    #print(stock_info.get_text())
    #print('')
    print(time_of_data.get_text())
    
    load_data(stock_name)
    
    
    
    
    #endregion

def getDB():
    file = 'commonstocks.csv'
    database = pd.read_csv(file, index_col = 0)

def compare(input):
    starhill_variable = str(input).split()
    
def load_data(stock_name):
    directory = 'stockdata'
    stocks = []
    
    #region load files
    for file_name in os.listdir(directory):
        file = os.path.join(directory, file_name)
        if file_name.strip('.csv') == stock_name:
            stocks.append(pd.read_csv(file))
        
    
    #endregion
    
    #region make prettier
    choice = input('what would you like to do: ')
    #first option pick any date
    match choice:
        case 'date':
            user_date = input('which date would you like to look at: ')
            
            for data in open(f'stockdata/{stock_name}.csv'):
                pattern = rf'({user_date},.+)'
                line = re.search(pattern,data)
                if line:
                    result = line.group()
                
            result = str(result).split(',')
            
            date_DB = pd.DataFrame({
                'date':result[0],
                'open':result[1],
                'high':result[2],
                'low':result[3],
                'close':result[4]
            },index = [0])
            
            print(date_DB)
            
        case '30,60,90':
            #take the file for loop each line
            result = []
            for i,data in enumerate(open(f'stockdata/{stock_name}.csv')):
                if i == 30:
                    result.append(data.split(','))
                if i == 60:
                    result.append(data.split(','))
                if i == 90:
                    result.append(data.split(','))
                
            date,high,low,open_price,close = [],[],[],[],[]
            for i in result:
                date.append(i[0])
                open_price.append(i[1])
                high.append(i[2])
                low.append(i[3])
                close.append(i[4])
            data_369 = pd.DataFrame({
                'Date':date,
                'High':high,
                'Low':low,
                'Open':open_price,
                'Close':close
            })
            print(data_369)
        case 'specific month':
            pass

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
        #TODO compare
        user_stock = input(f'what {choice} would you like to compare: ').upper()
        compare(user_stock)