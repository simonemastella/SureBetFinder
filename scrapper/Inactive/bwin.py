from bs4 import BeautifulSoup as bs4 #per scrap
import pandas as pd #per analizzare e creare dataframe
from requests_html import HTMLSession
import webbrowser

def scrapCampionato(num):
    campionato=["https://sports.bwin.it/it/sports/calcio-4/scommesse/italia-20/serie-a-42"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render()
        soup = bs4(res.html.html, 'html5lib')
        partite = soup.findAll("ms-event",{"class":"grid-event ms-active-highlight"})
        for partita in partite:
            link=partita.find("a",{"class":"grid-event-wrapper"}).get("href")
            dataora=partita.find("div",{"class":"badges-wrapper"}).getText().strip()
            match=partita.findAll("div",{"class":"participant"})
            match=match[0].getText().strip()+" - "+match[1].getText().strip()
            new_row = {'giorno':dataora, 'ora':dataora, 'match':match,'link':link}
            risultato = risultato.append(new_row, ignore_index=True)
    return risultato

if __name__ == '__main__':
    print(scrapCampionato(0))