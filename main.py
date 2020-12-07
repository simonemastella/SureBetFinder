import scrapper.williamhill as williamhill
import scrapper.snai as snai
import scrapper.sisal as sisal
# NON HA LA RICERCA CAMPIONATO MA SOLO LA RICERCA DA NOME E MANUALE
import scrapper.eurobet as eurobet
import scrapper.marathonbet as marbet
import scrapper.betfair as betfair
import pandas as pd
from difflib import SequenceMatcher
import os.path
from datetime import datetime


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def confusioni(corretta, df):
    df = df.reset_index(drop=True)
    res = "PARTITA NON PRESENTE..."
    massimo = 0
    for i in range(len(df)):
        link = df.at[i, 'link']
        ratio = similar(corretta, df.at[i, 'match'])
        if ratio > massimo:
            massimo = ratio
            res = link
    return res


def popolaPartita(riga):
    resp = pd.DataFrame(
        columns=['tipo', 'quota1', 'quota2', 'var', 'link1', 'link2'])
    quote_willhil = williamhill.scrap(riga.at['link_williamhill'])
    print("WILLHIAMHILL= OK")
    quote_snai = snai.scrap(riga.at['link_snai'])
    print("snai= OK")
    quote_sisal = sisal.scrap(riga.at['link_sisal'])
    print("sisal= OK")
    quote_marbet = marbet.scrap(riga.at['link_marbet'])
    print("marbet= OK")
    quote_betfair = betfair.scrap(riga.at['link_betfair'])
    print("betfair= OK")
    quote_eurobet= eurobet.scrap(riga.at['link_eurobet'])
    print("eurobet= OK")
    for i in range(len(quote_snai)):
        tipo = quote_snai.at[i, 'tipo']
        coppia_snai = quote_snai.query(
            "tipo=='"+tipo+"'").reset_index(drop=True)
        coppia_sisal = quote_sisal.query(
            "tipo=='"+tipo+"'").reset_index(drop=True)
        coppia_willhil = quote_willhil.query(
            "tipo=='"+tipo+"'").reset_index(drop=True)
        coppia_marbet = quote_marbet.query(
            "tipo=='"+tipo+"'").reset_index(drop=True)
        coppia_betfair = quote_betfair.query(
            "tipo=='"+tipo+"'").reset_index(drop=True)
        coppia_eurobet=quote_eurobet.query("tipo=='"+tipo+"'").reset_index(drop=True)
        if len(coppia_snai) < 1:
            snai_cv = 0
            snai_cf = 0
        else:
            snai_cv = float(coppia_snai.at[0, 'casoV'].replace(',', '.'))
            snai_cf = float(coppia_snai.at[0, 'casoF'].replace(',', '.'))
        if len(coppia_sisal) < 1:
            sisal_cv = 0
            sisal_cf = 0
        else:
            sisal_cv = float(coppia_sisal.at[0, 'casoV'].replace('-', '0'))
            sisal_cf = float(coppia_sisal.at[0, 'casoF'].replace('-', '0'))
        if len(coppia_willhil) < 1:
            willhill_cv = 0
            willhill_cf = 0
        else:
            willhill_cv = float(
                coppia_willhil.at[0, 'casoV'].replace(',', '.'))
            willhill_cf = float(
                coppia_willhil.at[0, 'casoF'].replace(',', '.'))
        if len(coppia_marbet) < 1:
            marbet_cv = 0
            marbet_cf = 0
        else:
            marbet_cv = float(coppia_marbet.at[0, 'casoV'].replace(',', '.'))
            marbet_cf = float(coppia_marbet.at[0, 'casoF'].replace(',', '.'))
        if len(coppia_betfair) < 1:
            betfair_cv = 0
            betfair_cf = 0
        else:
            betfair_cv = float(coppia_betfair.at[0, 'casoV'].replace(',', '.'))
            betfair_cf = float(coppia_betfair.at[0, 'casoF'].replace(',', '.'))
        if len(coppia_eurobet)<1:
            eurobet_cv=float(coppia_betfair.at[0, 'casoV'].replace(',', '.'))
            eurobet_cf=float(coppia_betfair.at[0, 'casoF'].replace(',', '.'))
        else:
            eurobet_cv=coppia_eurobet.at[0,'casoV']
            eurobet_cf=coppia_eurobet.at[0,'casoF']
        dV = {riga.at['link_snai']: snai_cv,
              riga.at['link_sisal']: sisal_cv,
              riga.at['link_williamhill']: willhill_cv,
              riga.at['link_marbet']: marbet_cv,
              riga.at['link_betfair']: betfair_cv, 
              riga.at['link_williamhill']:float(eurobet_cv)
              }  
        dF = {riga.at['link_snai']: snai_cf,
              riga.at['link_sisal']: sisal_cf,
              riga.at['link_williamhill']: willhill_cf,
              riga.at['link_marbet']: marbet_cf,
              riga.at['link_betfair']: betfair_cf , 
              riga.at['link_williamhill']:float(eurobet_cf)
              }    
        linkV = max(dV, key=dV.get)
        linkF = max(dF, key=dF.get)
        adV = dV.values()
        adF = dF.values()
        maxV = max(adV)
        maxF = max(adF)
        var = ((1/maxF) + (1/maxV))*100
        new_row = {'tipo': tipo, 'quota1': maxF, 'quota2': maxV,
                   'var': var, 'link1': linkF, 'link2': linkV}
        resp = resp.append(new_row, ignore_index=True)
    return resp


def getPartita(tabella, numero):
    return popolaPartita(tabella.iloc[numero])


def scaricaCampionato(numeroCampionato):
    date_williamhill = williamhill.scrapCampionato(numeroCampionato)
    print("WILLHIAMHILL= OK")
    date_snai = snai.scrapCampionato(numeroCampionato)
    print("SNAI= OK")
    date_sisal = sisal.scrapCampionato(numeroCampionato)
    print("SISAL= OK")
    date_marbet = marbet.scrapCampionato(numeroCampionato)
    print("MARBET= OK")
    date_betfair = betfair.scrapCampionato(numeroCampionato)
    print("BETFAIR= OK")
    date_eurobet = eurobet.scrapCampionatoManuale(numeroCampionato)
    print("eurobet= OK")
    tabella = pd.DataFrame(columns=['giorno',
                                    'ora',
                                    'match',
                                    'link_snai',
                                    'link_sisal',
                                    'link_williamhill',
                                    'link_marbet',
                                    'link_eurobet',
                                    'link_betfair'])
    numeroPartite = min(len(date_sisal), len(date_snai), len(
        date_williamhill),len(date_eurobet)) 
    for i in range(numeroPartite):
        giorno = date_snai.at[i, 'giorno']
        ora = date_snai.at[i, 'ora']
        match = date_snai.at[i, 'match']
        link_snai = date_snai.at[i, 'link']

        dfsisal = date_sisal.query("giorno=='"+giorno+"' and ora=='"+ora+"'")
        dfwillhil = date_williamhill.query(
            "giorno=='"+giorno+"' and ora=='"+ora+"'")
        dfmarbet = date_marbet.query("giorno=='"+giorno+"' and ora=='"+ora+"'")
        dfbetfair = date_betfair.query(
            "giorno=='"+giorno+"' and ora=='"+ora+"'")
        dfeurobet=date_eurobet.query("giorno=='"+giorno+"'")

        link_sisal = confusioni(match, dfsisal)
        link_williamhill = confusioni(match, dfwillhil)
        link_marbet = confusioni(match, dfmarbet)
        link_betfair = confusioni(match, dfbetfair)
        link_eurobet=confusioni(match, dfeurobet)

        new_row = {'giorno': giorno,
                   'ora': ora,
                   'match': match,
                   'link_snai': link_snai,
                   'link_sisal': link_sisal,
                   'link_williamhill': link_williamhill,
                   'link_marbet': link_marbet,
                   'link_betfair': link_betfair ,
                   'link_eurobet':link_eurobet}  
        tabella = tabella.append(new_row, ignore_index=True)
        tabella.to_csv('campionati/campionato' +
                       str(numeroCampionato)+'.csv', index=False)
    return tabella


def getCampionato(numeroCampionato):
    filename = 'campionati/campionato'+str(numeroCampionato)+'.csv'
    if os.path.isfile(filename):
        tabella = pd.read_csv(filename)
        giorno = tabella.at[0, 'giorno']
        ora = tabella.at[0, 'ora']
        if input("DATAFRAME TROVATO: ultima partita trovata risale al "+str(giorno)+" alle ore "+str(ora)+"\nDigita 'N' per scaricarne uno nuovo:  ") == "N":
            return scaricaCampionato(numeroCampionato)
        else:
            return tabella
    else:
        return scaricaCampionato(numeroCampionato)


def oneFromCampionato(tabella):
    scelta = int(input("Scegli quale partita vuoi: "))
    df=(getPartita(tabella, scelta))
    df.to_csv('partite/partita' + str(scelta)+'.csv', index=False)


def allFromCampionato(tabella):
    for i in range(len(tabella)):
        print("DEBUG MATCH NUMBER: "+str(i))
        df=(getPartita(tabella, i))
        df.to_csv('partite/partita' + str(i)+'.csv', index=False)

def init():
    numeroCampionato = int(input(
        "0) serie A\n01) serie b\n02) champions\n03) europa\n04-05) inghilterra\n06-07) spagna\n08-09) germania\n10-11) francia\n12-13) olanda\n14-15) portogallo\nInserisci il numero della partita: "))
    tabella = getCampionato(numeroCampionato)
    return tabella


if __name__ == '__main__':
    table=init()
    print(table)
    pick=input("Vuoi controllare solo una Partita('0') o tutto il Campionato('1')? ")
    if pick=='0':
        oneFromCampionato(table)
    elif pick=='1':
        allFromCampionato(table)
