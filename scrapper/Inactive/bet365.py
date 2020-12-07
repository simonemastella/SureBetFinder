import requests
import webbrowser
from bs4 import BeautifulSoup as bs4 #per scrap
import pandas as pd #per analizzare e creare dataframe
from requests_html import HTMLSession

'''
# Establish chrome driver and go to report site URL
link="https://www.bet365.it/#/AC/B1/C1/D8/E93855159/F3/I1/"
driver = webdriver.Chrome()
driver.get(link)
html = driver.page_source
soup = bs4(html)
risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
tags= soup.findAll("div",{"class":"gl-MarketGroupContainer "})
esatto=tags[2].findAll("span",{"class":"gl-Participant_Odds"})
doppia=tags[3].findAll("span",{"class":"gl-Participant_Odds"})
new_row = {'tipo':"1X-2", 'casoF':doppia[0].getText().strip(), 'casoV':esatto[2].getText().strip()}
risultato = risultato.append(new_row, ignore_index=True)
new_row = {'tipo':"12-X", 'casoF':doppia[2].getText().strip(), 'casoV':esatto[1].getText().strip()}
risultato = risultato.append(new_row, ignore_index=True)
new_row = {'tipo':"2X-1", 'casoF':doppia[1].getText().strip(), 'casoV':esatto[0].getText().strip()}
risultato = risultato.append(new_row, ignore_index=True)
'''







'''
risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
tags= soup.findAll("div",{"class":"gl-MarketGroupContainer "})
esatto=tags[2].findAll("span",{"class":"gl-Participant_Odds"})
doppia=tags[3].findAll("span",{"class":"gl-Participant_Odds"})
new_row = {'tipo':"1X-2", 'casoF':doppia[0].getText().strip(), 'casoV':esatto[2].getText().strip()}
risultato = risultato.append(new_row, ignore_index=True)
new_row = {'tipo':"12-X", 'casoF':doppia[2].getText().strip(), 'casoV':esatto[1].getText().strip()}
risultato = risultato.append(new_row, ignore_index=True)
new_row = {'tipo':"2X-1", 'casoF':doppia[1].getText().strip(), 'casoV':esatto[0].getText().strip()}
risultato = risultato.append(new_row, ignore_index=True)
return risultato









def scrap(link):
    session = HTMLSession()
    with session.get(link) as res:
        res.html.render() 
        soup = bs4(res.html.html, 'html5lib')
        print(res.html.text)
        risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
        tags= soup.findAll("div",{"class":"gl-MarketGroupContainer "})
        esatto=tags[2].findAll("span",{"class":"gl-Participant_Odds"})
        doppia=tags[3].findAll("span",{"class":"gl-Participant_Odds"})
        new_row = {'tipo':"1X-2", 'casoF':doppia[0].getText().strip(), 'casoV':esatto[2].getText().strip()}
        risultato = risultato.append(new_row, ignore_index=True)
        new_row = {'tipo':"12-X", 'casoF':doppia[2].getText().strip(), 'casoV':esatto[1].getText().strip()}
        risultato = risultato.append(new_row, ignore_index=True)
        new_row = {'tipo':"2X-1", 'casoF':doppia[1].getText().strip(), 'casoV':esatto[0].getText().strip()}
        risultato = risultato.append(new_row, ignore_index=True)
        print(risultato)




'''




"""
casa="Roma"
ospite="Benevento"
webbrowser.open("https://www.bet365.it/#/AX/K^"+casa+"%20"+ospite+"/")
cookie="rLaJXw==.r0M0c9KnPFuiWO85xnz5/Bugqpkt6sid6Gc9vHuNouI="
r=requests.get("https://www.bet365.it/api/1/sitesearch/query?lid=6&zid=0&pd=%23AX%23K%5E"+casa+"%2520"+ospite+"%23&cid=97&ctid=97", headers={
    "X-Net-Sync-Term":cookie,
    "Cookie": "aps03=0"})
contenuto=str(r.content).split
"""