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
            tags= soup.findAll("div",{"class":"TabellaEsitiRow-hvzh1w-0 jxwiSe"})
            esdop=tags[0].findAll("div",{"class":"EsitoButton-mp5c0x-0 dQZBRx"})
            new_row = {'tipo':"1X-2", 'casoF':esdop[3].getText(), 'casoV':esdop[2].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"12-X", 'casoF':esdop[5].getText(), 'casoV':esdop[1].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"2X-1", 'casoF':esdop[4].getText(), 'casoV':esdop[0].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            gng=tags[1].findAll("div",{"class":"EsitoButton-mp5c0x-0 dQZBRx"})
            new_row = {'tipo':"GOL/NOGOL", 'casoF':gng[1].getText(), 'casoV':gng[0].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            over=tags[2].findAll("div",{"class":"TabellaColumn-nrcwsc-0 iJTAjk"})
            under=tags[3].findAll("div",{"class":"TabellaColumn-nrcwsc-0 iJTAjk"})
            new_row = {'tipo':"UNDER/OVER 0.5", 'casoF':under[0].getText(), 'casoV':over[0].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 1.5", 'casoF':under[1].getText(), 'casoV':over[1].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 2.5", 'casoF':under[2].getText(), 'casoV':over[2].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 3.5", 'casoF':under[3].getText(), 'casoV':over[3].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 4.5", 'casoF':under[4].getText(), 'casoV':over[4].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
            new_row = {'tipo':"UNDER/OVER 5.5", 'casoF':under[5].getText(), 'casoV':over[5].getText()}
            risultato = risultato.append(new_row, ignore_index=True)
        return risultato
    except:
        session.close()
        print("Errore nella ricerca DATI su SISAL, cerco di nuovo")
        return scrap(link) 

def cerca(partita, cont=0):
    link=("https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=search:"+partita.replace(" ","%20")).strip()
    if cont>1:
        webbrowser.open(link)
        return input("Inserisci il link preciso della partita su SISAL: ")
    try:    
        session = HTMLSession()
        with session.get(link) as res:
            res.html.render() 
            soup = bs4(res.html.html, 'html5lib')
            tag= (soup.find("a",{"class":"AvvenimentoDetailWrapper-w9f4wf-0 bhgtKE"})).get("href")
        return "https://www.sisal.it"+tag
    except:
        print("Errore nella ricerca PARTITA su SISAL, cerco di nuovo")
        return cerca(partita, cont+1)

def scrapByName(partita):
    link=cerca(partita)
    return scrap(link)
    
def scrapCampionato(num):
    campionato=["https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:21",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:22",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:18",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:153",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:86",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:1",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:79",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:137",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:4",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:3",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:14",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:15",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:29",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:30",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:54",
    "https://www.sisal.it/scommesse-matchpoint?filtro=0&schede=man:1:190"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render() 
        soup = bs4(res.html.html, 'html5lib')
        partite= (soup.findAll("div",{"TabellaEsitiRow-hvzh1w-0 eyTFpO"}))
        for partita in partite:
            match=partita.find("span",{"class":"AvvenimentoDescription-rieyuj-0 clFosV"}).getText().strip()
            dataora=partita.find("span",{"class":"AvvenimentoDate-giucxs-0 iaSisn"}).getText().strip().split(" ")
            link ="https://www.sisal.it"+partita.find("a",{"class":"AvvenimentoDetailWrapper-w9f4wf-0 bhgtKE"}).get("href")
            ora=dataora[2]
            data=dataora[0].split("/")
            new_row = {'giorno':data[0], 'ora':ora, 'match':match,'link':link}
            risultato = risultato.append(new_row, ignore_index=True)
    if len(risultato)!=0:
        return risultato
    else:
        print("SISAL RIPROVO")
        return scrapCampionato(num)

if __name__ == '__main__':
    print(scrapCampionato(0))