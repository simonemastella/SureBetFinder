from bs4 import BeautifulSoup as bs4 #per scrap
import pandas as pd #per analizzare e creare dataframe
from requests_html import HTMLSession
import webbrowser


def scrap(link):
    try:    
        session = HTMLSession()
        with session.get(link) as res:
            res.html.render() 
            soup = bs4(res.html.html, 'html5lib')
            risultato=pd.DataFrame(columns=['tipo','casoF','casoV'])
            tags= soup.findAll("div",{"class":"box-sport"})
            esatto=tags[0].findAll("div",{"class":"quota"})
            doppia=tags[7].findAll("div",{"class":"quota"})
            gng=tags[2].findAll("div",{"class":"quota"})
            
            unox=doppia[0].getText().strip()
            duex=doppia[1].getText().strip()
            unodue=doppia[2].getText().strip()
            new_row = {'tipo':"1X-2", 'casoF':unox[2:], 'casoV':esatto[2].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"12-X", 'casoF':unodue[2:], 'casoV':esatto[1].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"2X-1", 'casoF':duex[2:], 'casoV':esatto[0].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"GOL/NOGOL", 'casoF':gng[1].getText().strip(), 'casoV':gng[0].getText().strip()}
            risultato = risultato.append(new_row, ignore_index=True)
            righe=tags[1].findAll("div",{"class":"riga-quota"})
            for riga in righe:
                riga=riga.findAll("div",{"class":"containerQuota"})
                tipo="UNDER/OVER "+riga[0].getText().strip()
                quotaF=riga[1].find("div",{"class":"quota"}).getText().strip()
                quotaV=riga[2].find("div",{"class":"quota"}).getText().strip()
                new_row = {'tipo':tipo, 'casoF':quotaF, 'casoV':quotaV}
                risultato = risultato.append(new_row, ignore_index=True)
        return risultato
    except:
        print("Errore nella ricerca DATI su EUROBET, cerco di nuovo")
        return scrap(link)


def cerca(partita, cont=0):
    link=("https://www.eurobet.it/it/scommesse/#!/cerca/"+partita.replace(" ","%20")).strip()
    if cont >1:
        webbrowser.open(link)
        return input("Inserisci il link preciso della partita su EUROBET: ")
    try:    
        session = HTMLSession()
        with session.get(link) as res:
            res.html.render() 
            soup = bs4(res.html.html, 'html5lib')
            tag= (soup.find("div",{"class":"event-exhibition"}))
        return "https://www.eurobet.it"+tag.find('a').get("href")
    except:
        print("Errore nella ricerca PARTITA su EUROBET, cerco di nuovo")
        return cerca(partita, cont+1)


def scrapByName(partita):
    link=cerca(partita)
    return scrap(link)

def scrapCampionato(num):
    campionato=["https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-a/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-b1/",
    "https://www.eurobet.it/it/scommesse/#!/manifestazione/champions-europa-league/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/eu-europa-league/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/ing-premier-league/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/ing-championship1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/es-liga/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/es-liga-adelante/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/de-bundesliga/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/de-2-bundesliga1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/fr-ligue-1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/fr-ligue-2/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/nl-eredivisie1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/nl-eerste-divisie/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/pt-primeira-liga/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/pt-segunda-divisao/"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render()
        soup = bs4(res.html.html, 'html5lib')
        giornate = soup.findAll("div",{"class":"anti-row"})
        giornate=giornate.pop(0)
        for giornata in giornate:
            dataora=giornata.find("div",{"class":"time-box"})
            dataora=dataora.findAll("p")
            if len(dataora)==1:
                data=0
                ora=dataora[0].getText()
            else:
                data=dataora[0].getText().split("/")
                ora=dataora[1].getText()
            matchelink= giornata.find("div",{"class":"event-players"})
            link=matchelink.find("a").get("href")
            match=matchelink.getText().strip()
            new_row = {'giorno':data[0], 'ora':ora, 'match':match.getText().strip(),'link':link}
            risultato = risultato.append(new_row, ignore_index=True)
    return risultato

def scrapCampionatoManuale(num):
    campionato=["https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-a/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-b1/",
    "https://www.eurobet.it/it/scommesse/#!/manifestazione/champions-europa-league/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/eu-europa-league/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/ing-premier-league/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/ing-championship1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/es-liga/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/es-liga-adelante/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/de-bundesliga/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/de-2-bundesliga1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/fr-ligue-1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/fr-ligue-2/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/nl-eredivisie1/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/nl-eerste-divisie/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/pt-primeira-liga/",
    "https://www.eurobet.it/it/scommesse/#!/calcio/pt-segunda-divisao/"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    webbrowser.open_new(campionato[num])
    input("Fatto?")
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    with open("src/eurobet.html", encoding="utf-8") as f:
        data = f.read()
        soup = bs4(data, 'html.parser')
        giornate = soup.findAll("div",{"class":"anti-row"})
        giornate.pop(0)
        for giornata in giornate:
            partite = giornata.findAll("div",{"class":"event-row"})
            for partita in partite:
                dataora=partita.find("div",{"class":"time-box"})
                dataora=dataora.findAll("p")
                if len(dataora)==1:
                    data=soup.find("h2",{"class":"title-event info-match"}).getText().split(" ")
                    data=data[1]
                    ora=dataora[0].getText()
                else:
                    data=dataora[0].getText().split("/")
                    data=data[0]
                    ora=dataora[1].getText()
                matchelink= partita.find("div",{"class":"event-players"})
                link="https://www.eurobet.it" + matchelink.find("a").get("href")
                match=matchelink.getText().strip()
                new_row = {'giorno':data, 'ora':ora, 'match':match,'link':link}
                risultato = risultato.append(new_row, ignore_index=True)
    if len(risultato)!=0:
        return risultato
    else:
        return scrapCampionato(num)

if __name__ == '__main__':
    print(scrapCampionatoManuale(8))


