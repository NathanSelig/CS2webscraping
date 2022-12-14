import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os


#region opening message
print('this program is used to not only see the value of stocks but also compare them to there popularity on Robinhood')
#endregion

#region functions
def stock_information(page, stock_name):
    user_soup = BeautifulSoup(page.content, 'html.parser') 
    #region price of stock
    stock_price  = user_soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')
    stock_info = user_soup.find('table', class_ = 'W(100%)')
    time_of_data = user_soup.find('div', id = 'quote-market-notice')
    
    print('')
    print(stock_price['value'], '  ')
    print(time_of_data.get_text())
    print('')
    
    info_DB = pd.DataFrame({
        'price':stock_price['value'],
        'time':time_of_data.get_text()
    },index = [0])
    
    return info_DB


def compare(input):
    starhill_variable = str(input).split()
    
    user_page1 = requests.get(f'https://finance.yahoo.com/quote/{starhill_variable[0]}')
    user_page2 = requests.get(f'https://finance.yahoo.com/quote/{starhill_variable[1]}')
    
    stock1_info = stock_information(user_page1,"")
    stock2_info = stock_information(user_page2,"")
    commonstocks1 = load_common(starhill_variable[0])
    commonstocks2= load_common(starhill_variable[1])
    
    stock1_all = pd.concat([stock1_info,commonstocks1], axis = 'columns')
    stock2_all = pd.concat([stock2_info,commonstocks2], axis = 'columns')
    
    joint_info = pd.concat([stock1_all, stock2_all])
    
    print(joint_info)
    
def load_data(stock_name):
    directory = 'stockdata'
    stocks = []
    
    for file_name in os.listdir(directory):
        file = os.path.join(directory, file_name)
        if file_name.strip('.csv') == stock_name:
            stocks.append(pd.read_csv(file))
        
    
    
    choice = input('what would you like to do: ')
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
        case '369':
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
        case 'month':
            month = input('what month would you like to look at: ')
            result = []
            for data in open(f'stockdata/{stock_name}.csv'):
                pattern = rf'2.-{month}.+'
                line = re.findall(pattern,data)
                if line:
                    result.append(str(line).split(','))
                
            
            date,high,low,open_price,close = [],[],[],[],[]
            for i in result:
                date.append(i[0])
                open_price.append(i[1])
                high.append(i[2])
                low.append(i[3])
                close.append(i[4])
            
                        
            data_month = pd.DataFrame({
                'Date':date,
                'High':high,
                'Low':low,
                'Open':open_price,
                'Close':close
            })
            
            print(data_month)
            
            

def load_common(stock_name):
    file = 'commonstocks.csv'
    database = pd.read_csv(file, index_col = 0)
    #make for loop for each line in file
    for data in open(file):
    #split the string and find symbol
        data = data.split(',')
    #if symbol == stock_name return row as pd DB
        if data[2].strip('\n') == stock_name:
            return pd.DataFrame({
                'rank':data[0],
                'name':data[1],
                'symbol':data[2].strip('\n')                
                
                },index = [0])
    
    
    
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
print('what are you looking for: \nstock\netf\ncompare')
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
    case 'compare':
        #TODO compare
        user_stock = input(f'what {choice} would you like to compare: ').upper()
        compare(user_stock)
