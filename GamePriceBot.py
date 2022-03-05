import requests
from bs4 import BeautifulSoup
import re

def steambot(inputname):
    search= inputname.replace(' ','+')
    url='https://store.steampowered.com/search/?term=' + search
    strhtml=requests.get(url)
    soup=BeautifulSoup(strhtml.text,'lxml')
    target = soup.select('#search_resultsRows>a:nth-child(1)>div.responsive_search_name_combined>div.col.search_name.ellipsis>span')

    if target == []:
        return {'GameName':'Game Not Found','Price':'','Onsale':''}
    
    else:
        gamename = target[0].get_text().strip()
        data = soup.select('#search_resultsRows>a:nth-child(1)>div.responsive_search_name_combined>div.col.search_price_discount_combined.responsive_secondrow>div.col.search_price.responsive_secondrow')[0]
        onsale = "No"
        result = data.get_text().strip()
        
        if result.lower() == 'free to play':
            price = 0
        elif result == "":
            price = "unavaliable"
        else:
            if data.get('class')[2] == 'discounted':
                onsale = "Yes"
                price = round(float(result.split(" ")[2]),2)
            else:
                price = float(result.split(" ")[1])
                
        returndata = {'GameName':gamename,'Price':price,'Onsale':onsale}
        return returndata
        
def epicbot(inputname):
    search= inputname.replace(' ','%20')
    url='https://www.epicgames.com/store/zh-Hant/browse?q={}&sortBy=relevancy'.format(search)
    strhtml=requests.get(url)
    soup=BeautifulSoup(strhtml.text,'lxml')
    target = soup.select('#dieselReactWrapper>div>div.css-xxkdgb>main>div:nth-child(2)>div>div>div>div>section>div>section>div>section>section>ul>li>div>div>div>a>div>div>div.css-hkjq8i>span>div')

    if target == []:
        return {'GameName':'Game Not Found','Price':'','Onsale':''}
        
    else:
        gamename = target[0].get_text().strip()
        data = soup.select('#dieselReactWrapper>div>div.css-xxkdgb>main>div:nth-child(2)>div>div>div>div>section>div>section>div>section>section>ul>li>div>div>div>a>div>div>div.css-hkjq8i>div>div>span>div>span')[0]
        result = data.get_text().strip()
        
        onsale = "No"
        discount = soup.select('#dieselReactWrapper>div>div.css-xxkdgb>main>div:nth-child(2)>div>div>div>div>section>div>section>div>section>section>ul>li>div>div>div>a>div>div>div.css-hkjq8i>div>div>div>span')
        
        if result == "免費":
            price = 0
        else:
            if discount == []:
                price = float(result.split("$")[1])
            else:
                onsale = "Yes"
                dislevel = re.sub('\D','',discount[0].get_text().strip())
                dismulti = 1 - (int(dislevel) / 100)
                origprice = float(result.split("$")[1])
                price = round((origprice * dismulti), 2)
        
        returndata = {'GameName':gamename,'Price':price,'Onsale':onsale}
        return returndata
    
if __name__ == "__main__":
    name = input("Input game's name: ")
    steambot(name)
    epicbot(name)