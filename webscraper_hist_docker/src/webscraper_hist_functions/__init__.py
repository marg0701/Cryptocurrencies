'''
###########################################################################################
##     In this section there are the functions to webcraping historical information      ##
##     prices of the cryptocurrencies                                                    ##
###########################################################################################
'''

# -------------------------------- Import Packages ----------------------------------------
import bs4 as bs
import urllib.request
import pandas as pd
import datetime

# -------------------------------- Functions ---------------------------------------------
def retrieve(coin, start_date, end_date):
    # Ensures proper formatting of user inputs
    coin = coin.lower()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    # Retrieves data with BeautifulSoup and parses
    url = 'https://coinmarketcap.com/currencies/' + coin + '/historical-data/?start=' + start_date + '&end='+end_date
    print(url)
    link = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(link, "html.parser")
    prices_table = soup.find_all('tr')
    # Creates list of dictionaries to feed into the DataFrame
    list_of_dic = []
    list_itemset = []

    for count, itemset in enumerate(prices_table):
        if count != 1:
            list_itemset.append(itemset)

    for itemset in list_itemset[2:]:
        souptest=bs.BeautifulSoup(str(itemset), 'html.parser')
        td_tables=souptest.find_all('td')
        date = td_tables[0].text
        opening = td_tables[1].text
        high = td_tables[2].text
        low = td_tables[3].text
        close = td_tables[4].text
        volume = td_tables[5].text
        marketcap = td_tables[6].text

        dictionary = {'Date' : date, 'Coin' : coin.capitalize(), 'Opening Price' : opening,'Closing Price' : close, 'Low' :
            low, 'High': high, 'Volume' : volume, 'Market Cap': marketcap}
        list_of_dic.append(dictionary)

     # Creates and sends our DataFrame
    df = pd.DataFrame(list_of_dic)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.iloc[:-19,:]
    return df
