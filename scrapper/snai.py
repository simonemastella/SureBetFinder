from bs4 import BeautifulSoup as bs4 #per scrap
import pandas as pd #per analizzare e creare dataframe
from requests_html import HTMLSession

def scrap(link):
    try:
        session = HTMLSession()
        with session.get(link) as res:
            res.html.render() 
            soup = bs4(res.html.html, 'html5lib')
            tags= soup.findAll("table",{"class":"table table-bordered table-condensed table-striped table-hover margin-bottom-10 ng-scope"})
            risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
            esatto=tags[0].findAll("span",{"class":"ng-binding ng-scope"})
            doppia=tags[1].findAll("span",{"class":"ng-binding ng-scope"})
            new_row = {'tipo':"1X-2", 'casoF':doppia[0].getText().strip(), 'casoV':esatto[2].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"12-X", 'casoF':doppia[2].getText().strip(), 'casoV':esatto[1].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"2X-1", 'casoF':doppia[1].getText().strip(), 'casoV':esatto[0].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            tipo=tags[2].find("div",{"class":"pull-left ng-binding"}).getText().strip()
            t=tags[2].findAll("span",{"class":"ng-binding ng-scope"})
            quotaF=t[1].getText().strip()
            quotaV=t[0].getText().strip()
            new_row = {'tipo':tipo, 'casoF':quotaF, 'casoV':quotaV}
            if "GOL" in tipo:
                risultato = risultato.append(new_row, ignore_index=True)
            for tag in tags[3:12]:
                tipo=tag.find("div",{"class":"pull-left ng-binding"}).getText().strip()
                t=tag.findAll("span",{"class":"ng-binding ng-scope"})
                quotaF=t[0].getText().strip()
                quotaV=t[1].getText().strip()
                new_row = {'tipo':tipo, 'casoF':quotaF, 'casoV':quotaV}
                if "UNDER" in tipo:
                    risultato = risultato.append(new_row, ignore_index=True)
            return risultato
    except:
        print("Errore nella ricerca DATI su SNAI, cerco di nuovo")
        session.close()
        return scrap(link)

def scrapCampionato(num):
    campionato=["https://www.snai.it/sport/CALCIO/SERIE%20A",
    "https://www.snai.it/sport/CALCIO/SERIE%20B",
    "https://www.snai.it/sport/CALCIO/CHAMPIONS%20LEAGUE",
    "https://www.snai.it/sport/CALCIO/EUROPA%20LEAGUE",
    "https://www.snai.it/sport/CALCIO/PREMIER%20LEAGUE",
    "https://www.snai.it/sport/CALCIO/CHAMPIONSHIP",
    "https://www.snai.it/sport/CALCIO/LIGA",
    "https://www.snai.it/sport/CALCIO/SPAGNA%202",
    "https://www.snai.it/sport/CALCIO/BUNDESLIGA",
    "https://www.snai.it/sport/CALCIO/GERMANIA%202",
    "https://www.snai.it/sport/CALCIO/LIGUE%201",
    "https://www.snai.it/sport/CALCIO/FRANCIA%202",
    "https://www.snai.it/sport/CALCIO/OLANDA%201",
    "https://www.snai.it/sport/CALCIO/OLANDA%202",
    "https://www.snai.it/sport/CALCIO/PORTOGALLO%201",
    "https://www.snai.it/sport/CALCIO/PORTOGALLO%202"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render() 
        soup = bs4(res.html.html, 'html5lib')
        date= (soup.findAll("div",{"class":"margin-bottom-3 ng-scope"}))
        for giorno in date:
            data=giorno.find("a",{"class":"btn btn-default btn-block text-left ng-binding"}).getText().strip()
            data=data.split("/")
            partite=giorno.findAll("div",{"class":"nopaddingLeftRight matchDescriptionFirstCol footballWidthFirstCol"})
            for partita in partite:
                ora=partita.find("span",{"class":"hourMatchFootball ng-binding"}).getText().strip()
                match=partita.find("span",{"class":"descriptionTextBlue"})
                link="https://www.snai.it"+(match.find("a",{"class":"ng-binding"})).get("href")
                new_row = {'giorno':data[0], 'ora':ora, 'match':match.getText().strip(),'link':link}
                risultato = risultato.append(new_row, ignore_index=True)
    if len(risultato)!=0:
        return risultato
    else:
        return scrapCampionato(num)

if __name__ == '__main__':
    print(scrapCampionato(0))
