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
            tags=soup.findAll("div",{"class":"market-inline-block-table-wrapper"})
            for tag in tags:
                titolo= tag.find("div",{"class":"name-field"})
                if titolo!= None:
                    titolo=titolo.getText().strip()
                    if "Risultato" == titolo:
                        esdop=tag.findAll("span",{"class":"selection-link active-selection"})
                        new_row = {'tipo':"1X-2", 'casoF':esdop[3].getText().strip(), 'casoV':esdop[2].getText().strip()}
                        risultato = risultato.append(new_row, ignore_index=True)
                        new_row = {'tipo':"12-X", 'casoF':esdop[4].getText().strip(), 'casoV':esdop[1].getText().strip()}
                        risultato = risultato.append(new_row, ignore_index=True)
                        new_row = {'tipo':"2X-1", 'casoF':esdop[5].getText().strip(), 'casoV':esdop[0].getText().strip()}
                        risultato = risultato.append(new_row, ignore_index=True)
                
                    elif "Gol" == titolo:
                        righe= tag.findAll("tr",{"data-header-highlighted-bounded":"true"})
                        for riga in righe:
                            tit=riga.find("td",{"nowrap":"nowrap"})
                            if tit!=None:
                                if "Entrambe le squadre segnano" ==  tit.getText().strip():
                                    gng=riga.findAll("td",{"class":"price height-column-with-price"})
                                    new_row = {'tipo':"GOL/NOGOL", 'casoF':gng[1].getText().strip(), 'casoV':gng[0].getText().strip()}
                                    risultato = risultato.append(new_row, ignore_index=True)


                    elif "Totale gol" == titolo:
                        uo=tag.findAll("div",{"class":"coeff-price"})
                        if len(uo)>4:
                            new_row = {'tipo':"UNDER/OVER 0.5", 'casoF':uo[0].getText().strip(), 'casoV':uo[1].getText().strip()}
                            risultato = risultato.append(new_row, ignore_index=True)
                            new_row = {'tipo':"UNDER/OVER 1.5", 'casoF':uo[2].getText().strip(), 'casoV':uo[3].getText().strip()}
                            risultato = risultato.append(new_row, ignore_index=True)
                            new_row = {'tipo':"UNDER/OVER 2.5", 'casoF':uo[4].getText().strip(), 'casoV':uo[5].getText().strip()}
                            risultato = risultato.append(new_row, ignore_index=True)
                            new_row = {'tipo':"UNDER/OVER 3.5", 'casoF':uo[6].getText().strip(), 'casoV':uo[7].getText().strip()}
                            risultato = risultato.append(new_row, ignore_index=True)
                            try:
                                new_row = {'tipo':"UNDER/OVER 4.5", 'casoF':uo[8].getText().strip(), 'casoV':uo[9].getText().strip()}
                                risultato = risultato.append(new_row, ignore_index=True)
                            except:
                                pass
                            
        return risultato
    
 

    
def scrapCampionato(num):
    campionato=["https://www.marathonbet.it/it/popular/Football/Italy/Serie+A+-+22434",
    "https://www.marathonbet.it/it/popular/Football/Italy/Serie+B+-+46723",
    "https://www.marathonbet.it/it/popular/Football/Clubs.+International/UEFA+Champions+League+-+21255",
    "https://www.marathonbet.it/it/popular/Football/Clubs.+International/UEFA+Europa+League+-+21366",
    "https://www.marathonbet.it/it/popular/Football/England/Premier+League+-+21520",
    "https://www.marathonbet.it/it/popular/Football/England/Championship+-+22807",
    "https://www.marathonbet.it/it/popular/Football/Spain/Primera+Division+-+8736",
    "https://www.marathonbet.it/it/popular/Football/Spain/Segunda+Division+-+48300",
    "https://www.marathonbet.it/it/popular/Football/Germany/Bundesliga+-+22436",
    "https://www.marathonbet.it/it/popular/Football/Germany/Bundesliga+2+-+42528",
    "https://www.marathonbet.it/it/popular/Football/France/Ligue+1+-+21533",
    "",
    "https://www.marathonbet.it/it/popular/Football/Netherlands/Eredivisie+-+38090",
    "https://www.marathonbet.it/it/popular/Football/Netherlands/Eerste+Divisie+-+345004",
    "https://www.marathonbet.it/it/popular/Football/Portugal/Primeira+Liga+-+43058",
    "https://www.marathonbet.it/it/popular/Football/Portugal/National+Championship+-+1916077"]
    #italia, champions e europa, inghilterra, spagna, germania, francia, olanda, portogallo
    if campionato[num] == "":
        return 0
    risultato=pd.DataFrame(columns=['giorno','ora','match','link'])
    session = HTMLSession()
    with session.get(campionato[num]) as res:
        res.html.render() 
        soup = bs4(res.html.html, 'html5lib')
        partite=(soup.findAll("table",{"class":"member-area-content-table"}))
        #print("vuoto?",len(partite))
        #print(len(giornate))
        for partita in partite:
            match=partita.findAll("span",{"data-member-link":"true"})
            match=match[0].getText().strip()+" - "+match[1].getText().strip()
            link ="https://www.marathonbet.it"+partita.find("a",{"class":"member-link"}).get("href")
            dataora=partita.find("td",{"class":"date"}).getText().strip().split(" ")    
            if len(dataora)==1:
                d = datetime.now()
                data=d.strftime("%d")
                ora=dataora[0]
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
    
    print(scrap("https://www.marathonbet.it/it/betting/Football/Italy/Serie+A/Lazio+vs+Juventus+-+10661623"))