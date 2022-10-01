import requests
from bs4 import BeautifulSoup
import pandas as pd


page = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.Yyyh9nbMI2w')
print(page.status_code)

soup = BeautifulSoup(page.content , 'html.parser')

seven_day_forecast = soup.find( id = 'seven-day-forecast-container')

forecast_items = seven_day_forecast.find_all(class_="tombstone-container")


tonight = forecast_items[0]


period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

print(period)
print(short_desc)
print(temp)

img = tonight.find("img")
desc = img['title']
print(desc)

period_tags = seven_day_forecast.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]


short_descs = [sd.get_text() for sd in seven_day_forecast.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day_forecast.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day_forecast.select(".tombstone-container img")]
print(short_descs)
print(temps)
print(descs)



weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc":descs
    })


print(weather)





