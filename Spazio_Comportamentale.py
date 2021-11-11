import copy

import strutture_dati
from strutture_dati import *
import CreaReteJSON as conv_json

stampa=""#conterrà il risultato finale
def spazio_comportamentale(rete,stampare=0):
    global stampa

    # if not (isinstance(rete,strutture_dati.Rete)):
    #     stampa += "Il file inserito non è una rete valida"
    #     if stampare == 1:
    #         print(stampa)
    #     return 0

    stampa += "Spazio comportamentale relativo a "+rete.nome+"\n\n"

    #Inizializzazione variabili utili
    lista_nodi=[]
    stati_iniziali=[]
    lista_link=[]
    lista_cammini=[]

    #Lo stato iniziale dello spazio conterrà gli stati iniziali degli FA presi in considerazione
    for FA in rete.lista_FA:
        stati_iniziali.append(FA.stato_iniziale.nome)

    #Lo stato iniziale dello spazio conterrà l'unione dei link degli FA presi in considerazione
    for link in rete.lista_link:
        lista_link.append(link)

    #Creo il nodo iniziale dello spazio come unione di stati iniziali e lista link
    nodo_iniziale=Nodo(stati_FA=stati_iniziali,lista_link=lista_link)
    nodo_iniziale.final=True

    #Il nodo iniziale sarà il primo nodo dello spazio, lista nodi sarà una struttura contenente permanentemente i nodi trovati
    lista_nodi.append(nodo_iniziale)

    #Creo una coda nodi come struttura provvisoria per svolgere le operazioni sui nodi
    coda_nodi=[]
    coda_nodi.append(nodo_iniziale)

    #Eseguo operazioni sulla coda nodi per ricavare i nuovi nodi partendo da quello iniziale
    while coda_nodi:

        nodo_attuale=coda_nodi[0]

        id_FA=0#attraverso l'id riferenzio il FA su cui son svolte le operazioni


        for stato_FA in nodo_attuale.stati_FA: #per ogni stato del FA
            if id_FA < (len(rete.lista_FA)):
                FA=rete.lista_FA[id_FA]#seleziono il FA su cui lavorare
                for transizione in FA.transizioni: #per ogni transizione del FA
                    if transizione.stato_i.nome==stato_FA:#Se lo stato iniziale della transizione presa in considerazione è uguale allo stato attuale del FA
                        nuovo_nodo=crea_nodo(nodo_attuale, transizione, id_FA, rete.lista_link)#Richiamo la funzione per creare un nuovo nodo
                        if nuovo_nodo is not None: #Se il nodo viene creato correttamente avanzo nell'algoritmo
                            finale=True
                            for nuovo_link in nuovo_nodo.lista_link: #Controllo che il nodo sia finale e definisco l'attributo final
                                if nuovo_link.buffer != '':
                                    finale=False
                            nuovo_nodo.final=finale
                            # Se il nodo non è già presente in lista nodi viene appeso alla lista e alla coda dei nodi
                            if not any(nodo for nodo in lista_nodi if nodo.nome==nuovo_nodo.nome):
                                lista_nodi.append(nuovo_nodo)
                                coda_nodi.append(nuovo_nodo)

                            #Creo il cammino che porta al nuovo nodo
                            nuovo_cammino = Cammino(nodo_attuale, nuovo_nodo, nome=transizione.nome, oss=transizione.oss, ril=transizione.ril)
                            lista_cammini.append(nuovo_cammino)

            id_FA+=1
        #Rimuovo il nodo appena studiato
        coda_nodi.remove(nodo_attuale)

    #Fine While

    #Eseguo la potatura sui nodi e i cammini appena trovati
    lista_nodi,lista_cammini=potatura(lista_nodi,lista_cammini)

    #Assegno un id a ogni nodo a seguito della potatura, così da non avere valori discontinui
    id_nodo=0
    for nodo in lista_nodi:
        nodo.id=id_nodo
        for cammino in lista_cammini:
            if nodo.nome==cammino.nodo_iniziale.nome:
                cammino.nodo_iniziale.id=nodo.id
            if nodo.nome==cammino.nodo_finale.nome:
                cammino.nodo_finale.id=nodo.id
        id_nodo+=1


    #Riempio stampa che verrà restituito nell'output
    stampa+="Numero nodi trovati: "+str(len(lista_nodi))+"\n"
    for nodo in lista_nodi:
        stampa+="ID :"+str(nodo.id)+"\t "+"Nome: "+ nodo.nome + "\n"
    stampa+="\n"
    stampa+="Numero cammini trovati: "+str(len(lista_cammini))+"\n"
    for cammino in lista_cammini:
        stampa+="Nodo iniziale: "+str(cammino.nodo_iniziale.id) +"\t "+"Nome: "+ cammino.nome + "\t"+ "Nodo finale: "+str(cammino.nodo_finale.id)+"\t"+"Oss: "+cammino.oss+"\t"+"Ril: "+cammino.ril+"\n"
    if stampare==1:
        print(stampa)

    #Salvo i RisultatiTXT del metodo in file .txt e l'oggetto creato in file .json
    #Fine metodo, restituisco lo spazio creato
    formato_testo = ".txt"
    nome_file="Comportamentale-"+rete.nome
    with open("RisultatiTXT/"+nome_file+formato_testo, 'w',encoding='utf-8') as f:
        f.write(stampa)
    formato_json = ".json"
    risultato = SpazioComportamentale(nodo_iniziale, lista_nodi, lista_cammini, rete.nome)
    conv_json.CreaJSONdaRete("RisultatiJSON/" + nome_file + formato_json, risultato)
    return SpazioComportamentale(nodo_iniziale, lista_nodi, lista_cammini,rete.nome)

#Funzione per eseguire la potatura
def potatura(lista_nodi,lista_cammini):
    global stampa
    stampa+="Nodi e cammini potati: "
    lista_nodi_potata = []#Conterrà tutti i nodi legittimi presi da lista nodi
    finito = False
    lista_nodi_eliminati=[]#Contiene nodi eliminati per poterli stampare
    lista_cammini_eliminati=[]#Contiene nodi eliminati per poterli stampare

    # creiamo la lista di nodi non finali per poi potare
    while finito is False:
        finito = True
        for nodo in lista_nodi:
            for cammino in lista_cammini:
                if nodo.nome == cammino.nodo_iniziale.nome or nodo.final is True:#Se il nodo è iniziale per qualche cammino o il nodo è di accettazione
                    if not any(nodo_pot for nodo_pot in lista_nodi_potata if nodo.nome==nodo_pot.nome):#Se il nodo non è già presente nella lista dei nodi potati
                        lista_nodi_potata.append(nodo)#Aggiungo il nodo alla lista dei nodi potati



        for nodo in lista_nodi:
            if not any(nodo_pot for nodo_pot in lista_nodi_potata if nodo.nome == nodo_pot.nome):#Se ci son nodi presenti in lista_nodi ma non in lista_nodi_potata
                for cammino in lista_cammini:
                    if cammino.nodo_finale.nome == nodo.nome:
                        lista_cammini.remove(cammino)#Elimino il cammino che ha come nodo finale il nodo non presente in lista nodi potata
                        lista_cammini_eliminati.append(cammino)
                        if not any(nodo_pot for nodo_pot in lista_nodi_eliminati if nodo.nome == nodo_pot.nome):  # Se il nodo non è già presente nella lista dei nodi potati
                            lista_nodi_eliminati.append(nodo)
                        finito = False
            # else:
            #     if not any(nodo_pot for nodo_pot in lista_nodi_eliminati if nodo.nome == nodo_pot.nome):  # Se il nodo non è già presente nella lista dei nodi potati
            #         lista_nodi_eliminati.append(nodo)  # Aggiungo il nodo alla lista dei nodi potati
        lista_nodi=copy.deepcopy(lista_nodi_potata) #Sovrascrivo lista_nodi_potata in lista_nodo
        lista_nodi_potata=[]
    #Fine While

    stampa += "Numero nodi potati: " + str(len(lista_nodi_eliminati)) + "\n"
    for nodo in lista_nodi_eliminati:
        stampa +="Nome: " + nodo.nome + "\n"
    stampa += "\n"
    stampa += "Numero cammini potati: " + str(len(lista_cammini_eliminati)) + "\n"
    for cammino in lista_cammini_eliminati:
        stampa += "Nodo iniziale: " + str(
            cammino.nodo_iniziale.nome) + "\t " + "Nome: " + cammino.nome + "\t" + "Nodo finale: " + str(
            cammino.nodo_finale.nome) + "\n"
    stampa+="\n"

    return lista_nodi,lista_cammini

#Funzione per la creazione di un nuovo nodo
def crea_nodo(nodo, transizione, id_FA, rete_lista_link):

    #Copio le liste su cui si andrà a lavorare prendendole dal nodo passato in ingresso
    lista_nuovi_stati=copy.deepcopy(nodo.stati_FA)
    lista_nuovi_link=copy.deepcopy(nodo.lista_link)

    #Se la transizione non scatta su evento vuoto
    if transizione.evento_in.evento.nome != "":
        link_funzione = transizione.evento_in.link
        evento_funzione = transizione.evento_in.evento
        indice_link = rete_lista_link.index(link_funzione)
        if lista_nuovi_link[indice_link].buffer != evento_funzione.nome:#Se il buffer del link è diverso dall'evento in ingresso della transizione non si crea il nodo
            return None
        else: #altrimenti svuoto il link in attesa di un nuovo evento
            lista_nuovi_link[indice_link].buffer = ''

    funzioni_out = transizione.eventi_out.copy()
    for funzione_out in funzioni_out: #Per ogni evento in uscita da una transizione
        link_funzione = funzione_out.link
        evento_funzione = funzione_out.evento

        indice_link = rete_lista_link.index(link_funzione)
        if lista_nuovi_link[indice_link].buffer != '': #se il buffer è vuoto non viene creato un nuovo nodo
            return None
        else: #altrimenti riempio il buffer del link con il nome dell'evento in uscita alla transizione
            lista_nuovi_link[indice_link].buffer = evento_funzione.nome

    #Creo gli attributi del nuovo nodo e lo ritorno alla funzione chiamante
    nuovi_stati = transizione.stato_f.nome
    lista_nuovi_stati[id_FA] = nuovi_stati

    return Nodo(lista_nuovi_stati,lista_nuovi_link)







