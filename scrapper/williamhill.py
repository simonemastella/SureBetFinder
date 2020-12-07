from bs4 import BeautifulSoup as bs4 #per scrap
import pandas as pd #per analizzare e creare dataframe
from requests_html import HTMLSession

def scrap(link):
    if True:    
        session = HTMLSession()
        with session.get(link) as res:
            res.html.render() 
            risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
            soup = bs4(res.html.html, 'html5lib')
            tags= soup.findAll("div",{"class":"btmarket"})
            esatto=tags[0].findAll("span",{"class":"betbutton__odds"})
            doppia=tags[1].findAll("span",{"class":"betbutton__odds"})
            new_row = {'tipo':"1X-2", 'casoF':doppia[0].getText().strip(), 'casoV':esatto[2].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"12-X", 'casoF':doppia[2].getText().strip(), 'casoV':esatto[1].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"2X-1", 'casoF':doppia[1].getText().strip(), 'casoV':esatto[0].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            tags= soup.findAll("div",{"class":"btmarket__wrapper btmarket--customised-2col -expanded"})
            uo=tags[0].findAll("span",{"class":"betbutton__odds"})
            gng=tags[1].findAll("span",{"class":"betbutton__odds"})
            new_row = {'tipo':"GOL/NOGOL", 'casoF':gng[1].getText(), 'casoV':gng[0].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 2.5", 'casoF':uo[0].getText(), 'casoV':uo[1].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
        session.close()
        return (risultato)

def scrapCampionato(num):
    campionato=["https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY321/Serie-A/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY23532/Serie-B/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY344/UEFA-Champions-League/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY1935/UEFA-Europa-League/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY295/Inghilterra-Premier-League/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY292/Inghilterra-Championship/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY338/Spagna-La-Liga/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY32982/Spagna-La-Liga-2/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY315/Germania-Bundesliga/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY317/Germania-Bundesliga-2/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY312/Francia-Ligue-1/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY314/Francia-Ligue-2/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY306/Olanda-Eredivisie/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY1073/Olanda-Eerste-Divisie/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY331/Portogallo-Primeira-Liga/matches/OB_MGMB/Esito-Finale",
    "https://sports.williamhill.it/betting/it-it/football/competitions/OB_TY332/Portogallo-Segunda-Liga/matches/OB_MGMB/Esito-Finale"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render() 
        soup = bs4(res.html.html, 'html5lib')
        date= (soup.findAll("div",{"data-test-id":"events-group"}))
        for giorno in date:
            data=giorno.find("div",{"class":"sp-o-market__title"}).getText().strip()
            data=data.split(" ")
            partite=giorno.findAll("article",{"class":"sp-o-market sp-o-market--default"})
            for partita in partite:
                ora=partita.find("aside",{"class":"sp-o-market__clock"}).getText().strip()
                match=partita.find("main",{"class":"sp-o-market__title"})
                link="https://sports.williamhill.it"+(match.find("a")).get("href")
                new_row = {'giorno':data[1], 'ora':ora, 'match':match.getText().replace('₋','-').strip(),'link':link}
                risultato = risultato.append(new_row, ignore_index=True)
    if len(risultato)!=0:
        return risultato
    else:
        return scrapCampionato(num)

if __name__ == '__main__':
    for i in range(10,0,-1):
        print(scrapCampionato(i))
