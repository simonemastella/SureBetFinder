from bs4 import BeautifulSoup as bs4 #per scrap
import pandas as pd #per analizzare e creare dataframe
from requests_html import HTMLSession
import webbrowser
from datetime import datetime, timedelta

def scrap(link):
    if True:    
        session = HTMLSession()
        with session.get(link) as res:
            res.html.render() 
            soup = bs4(res.html.html, 'html5lib')
            risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
            tags= soup.findAll("div",{"class":"mod yui3-widget yui3-module yui3-minimarketview"})
            esatto=(tags[0].findAll("li",{"class":"runner-item"}))
            esa=[]
            for ex in esatto:
                esa.append(ex.find("a"))
            dopppia=tags[4].findAll("li",{"class":"runner-item"})#1x 2x 12
            dopcha=[]
            for dc in dopppia:
                dopcha.append(dc.find("a"))
            golng=tags[1].findAll("li",{"class":"runner-item"})
            gng=[]
            for cc in golng:
                gng.append(cc.find("a"))
            new_row = {'tipo':"1X-2", 'casoF':dopcha[0].getText().strip(), 'casoV':esa[2].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"12-X", 'casoF':dopcha[2].getText().strip(), 'casoV':esa[1].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"2X-1", 'casoF':dopcha[1].getText().strip(), 'casoV':esa[0].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"GOL/NOGOL", 'casoF':gng[1].getText().strip(), 'casoV':gng[0].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)

            balla=soup.find("div",{"class":"runner-markets-container"}) 
            under=balla.findAll("li",{"class":"runner runner-group-0 runner-index-1"})
            over=balla.findAll("li",{"class":"runner runner-group-0 runner-index-0"})
            for ind in range(len(under)):
                if under[ind].getText().strip()=="":
                    under[ind]='1'
                else:
                    under[ind]=under[ind].getText().strip()
                if over[ind].getText().strip()=="":
                    over[ind]='1'
                else:
                    over[ind]=over[ind].getText().strip()
            new_row = {'tipo':"UNDER/OVER 0.5", 'casoF':under[1], 'casoV':over[1]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 1.5", 'casoF':under[2], 'casoV':over[2]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 2.5", 'casoF':under[3], 'casoV':over[3]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 3.5", 'casoF':under[4], 'casoV':over[4]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 4.5", 'casoF':under[5], 'casoV':over[5]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 5.5", 'casoF':under[6], 'casoV':over[6]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 6.5", 'casoF':under[7], 'casoV':over[7]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 7.5", 'casoF':under[8], 'casoV':over[8]}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 8.5", 'casoF':under[9], 'casoV':over[9]}
            risultato = risultato.append(new_row, ignore_index=True)
        return risultato

 

    
def scrapCampionato(num):
    campionato=["https://www.betfair.it/sport/football/italia-serie-a/81",
    "https://www.betfair.it/sport/football/italia-serie-b/12199689",
    "https://www.betfair.it/sport/football/uefa-champions-league/228",
    "https://www.betfair.it/sport/football/uefa-europa-league/2005",
    "https://www.betfair.it/sport/football/inghilterra-premier-league/10932509",
    "https://www.betfair.it/sport/football/inghilterra-championship/7129730",
    "https://www.betfair.it/sport/football/spagna-la-liga/117",
    "https://www.betfair.it/sport/football/spagna-segunda-division/12204313",
    "https://www.betfair.it/sport/football/germania-bundesliga/59",
    "https://www.betfair.it/sport/football/germania-bundesliga-2/61",
    "https://www.betfair.it/sport/football/francia-ligue-1/55",
    "https://www.betfair.it/sport/football/francia-ligue-2/57",
    "https://www.betfair.it/sport/football/olanda-eredivisie/9404054",
    "https://www.betfair.it/sport/football/olanda-eerste-divisie/11",
    "https://www.betfair.it/sport/football/portogallo-primeira-liga/99",
    "https://www.betfair.it/sport/football/portogallo-segunda-liga/9513"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render() 
        soup = bs4(res.html.html, 'html5lib')
        giornate=(soup.findAll("ul",{"class":"event-list"}))
        #print(len(giornate))
        for giornata in giornate:
            partite= (giornata.findAll("li",{"class":"com-coupon-line-new-layout betbutton-layout avb-row avb-table market-avb quarter-template market-2-columns"}))
            partite.append(giornata.find("li",{"class":"com-coupon-line-new-layout betbutton-layout avb-row avb-table last market-avb quarter-template market-2-columns"}))
            for partita in partite:
                match=partita.findAll("span",{"class":"team-name"})
                match=match[0].getText().strip()+" - "+match[1].getText().strip()

                link ="https://www.betfair.it"+partita.find("a",{"class":"ui-nav event-team-container ui-top event-link ui-gtm-click"}).get("href")

                dataora=partita.find("span",{"class":"date ui-countdown"}).getText().strip().split(" ")
                
                if "Inizio" in dataora[0]:
                    d = datetime.now()
                    data=d.strftime("%d")
                    ora=dataora[2]
                elif len(dataora)==1:
                    d = datetime.now()
                    data=d.strftime("%d")
                    ora=dataora[0]
                elif len(dataora)==2:
                    d = datetime.now()+timedelta(days=1)
                    data=d.strftime("%d")
                    ora=dataora[1]
                else:
                    data=dataora[0]
                    ora=dataora[2]

                new_row = {'giorno':data, 'ora':ora, 'match':match,'link':link}
                risultato = risultato.append(new_row, ignore_index=True)     
    if len(risultato)!=0:
        return risultato
    else:
        return scrapCampionato(num)
   

if __name__ == '__main__':
    print(scrap("https://www.betfair.it/sport/football/uefa-champions-league/krasnodar-siviglia/30108296"))