import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0' }

# on test avec AAPL et MSFT
url = 'https://fr.finance.yahoo.com/quote/aapl'

r = requests.get(url,headers=headers)

soup = BeautifulSoup(r.text, 'html.parser')

print(soup.title.text)

# On cherche dans le html où se trouve les données que l'on veut extraire
# Phase préliminaire, retour des prix et des % change 
price = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
print(price)

change = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text,
print(change)

# test pour le after market, il semble que la classe soit la même pour tous les tickers, le HTML est de même format quelque soit le ticker

price_after = soup.find('fin-streamer', {'class': 'C($primaryColor) Fz(24px) Fw(b)'}).text
print(price_after)

change_after = soup.find('div', {'class': 'Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)'}).find_all('fin-streamer')[3].text,
print(change_after)

# Automatisation
mystocks = ['AAPL', 'MSFT','TSLA','AMD','GME']
stockdata = []

def getData(symbol) :
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0' }

    # utilisation d'un f string pour automatiser
    url = f'https://fr.finance.yahoo.com/quote/{symbol}'

    r = requests.get(url,headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')

    stock = {
        'symbol' : symbol,
        'price' : soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text,
        'change' : soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text,
        'price after' : soup.find('fin-streamer', {'class': 'C($primaryColor) Fz(24px) Fw(b)'}).text,
        'change after' : soup.find('div', {'class': 'Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)'}).find_all('fin-streamer')[3].text,
    }
    return stock

# Boucle pour automatiser l'import 
for item in mystocks :
    stockdata.append(getData(item))
    print('Getting : ', item)

print(stockdata)

# mettre sous forme json les données incorporées
with open('stockdata.json', 'w') as f:
    json.dump(stockdata,f)

print('.Fin')

# mettre en dataframe pandas

stockdata_df = pd.DataFrame(stockdata)
print(stockdata_df)

# transfert en csv 

stockdata_df.to_csv(r'C:\Users\alrem\Desktop\Webscrapping\stockdata.csv', index=False)