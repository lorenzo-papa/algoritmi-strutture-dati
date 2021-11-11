import copy
import strutture_dati
from strutture_dati import *
stampa = "" #conterrà il risultato finale
import CreaReteJSON as conv_json
def osservazione_lineare(rete,osservazione,stampare=0):
    global stampa
    stringaOss=""
    stringa_nome_file=""
    for label in osservazione:
        stringaOss+=label+", "
        stringa_nome_file+=label
    stringaOss=stringaOss[:-2]

    # #gestione eccezioni
    # if not (isinstance(rete,strutture_dati.Rete)):
    #     stampa += "Il file inserito non è una rete valida"
    #     if stampare == 1:
    #         print(stampa)
    #     return 0
    stampa += "Spazio comportamentale relativo all'osservazione ["+ stringaOss+"]" +" e alla rete "+rete.nome + "\n\n"  # conterrà il risultato finale


    lista_nodi=[]
    stati_iniziali=[]
    lista_link=[]
    lista_cammini=[]

    #controllo iniziale per verificare che la lista di osservazioni passata in ingresso sia coerente con le etichette della rete
    for label in osservazione:
        label_esistente = False
        for FA in rete.lista_FA:
            for transizione in FA.transizioni:
                if transizione.oss == label:
                    label_esistente = True
        if label_esistente == False:
            stampa += "L'etichetta " + label + " non è presente tra le possibili etichette di osservabilità"
            if stampare==1:
                print(stampa)
            #risultato= {}
            return 0

    #Creo lo stato iniziale
    for FA in rete.lista_FA:
        stati_iniziali.append(FA.stato_iniziale.nome)

    for link in rete.lista_link:
        lista_link.append(link)

    nodo_iniziale=Nodo(stati_FA=stati_iniziali,lista_link=lista_link)
    nodo_iniziale.final=False
    lista_nodi.append(nodo_iniziale)


    coda_nodi=[]#Struttura provvisoria per eseguire le operazioni sui nodi
    coda_nodi.append(nodo_iniziale)

    while coda_nodi:
        nodo_attuale=coda_nodi[0]
        id_FA=0#Indice per idetificare il FA su cui si andrà a lavorare
        for stato_FA in nodo_attuale.stati_FA:
            if id_FA < (len(rete.lista_FA)):
                FA=rete.lista_FA[id_FA]
                for transizione in FA.transizioni:
                    if transizione.stato_i.nome==stato_FA:#Se una transizione ha lo stato di inizio uguale all'attuale stato dell'FA
                        if transizione.oss in osservazione and (nodo_attuale.indice_oss < len(osservazione)): #Se l'indice di osservazione non ha raggiunto il valore massimo
                            if transizione.oss == osservazione[nodo_attuale.indice_oss]:#Se l'etichetta di osservabilità esaminata è presente nella giusta posizione nel vettore di osservazione linare
                                nuovo_nodo=crea_nodo(nodo_attuale, transizione, id_FA, rete.lista_link)
                            else:
                                nuovo_nodo = None
                        elif transizione.oss =='\u03b5':#anche se la transizione ha etichetta vuota creo il nuovo nodo
                            nuovo_nodo=crea_nodo(nodo_attuale, transizione, id_FA, rete.lista_link)
                        else:
                            nuovo_nodo=None
                        if nuovo_nodo is not None:
                            finale=True #verifico l'attributo final di ogni nodo
                            if nuovo_nodo.indice_oss != len(osservazione):
                                finale=False
                            for nuovo_link in nuovo_nodo.lista_link:
                                if nuovo_link.buffer != '':
                                    finale=False
                            nuovo_nodo.final=finale

                            if not any(nodo for nodo in lista_nodi if (nodo.nome==nuovo_nodo.nome and nodo.indice_oss==nuovo_nodo.indice_oss)):#se non ci sono già nodi uguali in lista nodi appendo il nodo appena creato
                                lista_nodi.append(nuovo_nodo)
                                coda_nodi.append(nuovo_nodo)

                            nuovo_cammino = Cammino(nodo_attuale, nuovo_nodo, nome=transizione.nome, oss=transizione.oss, ril=transizione.ril) #creo e appendo il nuovo cammino
                            lista_cammini.append(nuovo_cammino)

            id_FA+=1

        coda_nodi.remove(nodo_attuale)#tolgo dalla coda il nodo appena esaminato

    lista_nodi,lista_cammini=potatura(lista_nodi,lista_cammini)#eseguo potatura su nodi e cammini

    id_nodo=1#assegno ai nodi legittimi un id
    for nodo in lista_nodi:
        nodo.id=id_nodo
        for cammino in lista_cammini:
            if nodo.nome==cammino.nodo_iniziale.nome and nodo.indice_oss ==cammino.nodo_iniziale.indice_oss:
                cammino.nodo_iniziale.id=nodo.id
            if nodo.nome==cammino.nodo_finale.nome and nodo.indice_oss ==cammino.nodo_finale.indice_oss:
                cammino.nodo_finale.id=nodo.id
        id_nodo+=1

    if len(lista_nodi) ==0:
        stampa+="L'osservazione lineare non ha prodotto alcuna rete\n"
        if stampare==1:
            print(stampa)
        #risultato= {}
        return 0
    stampa+="Numero nodi generati: "+str(len(lista_nodi)) +"\n"
    for nodo in lista_nodi:
        stampa+="ID :"+str(nodo.id)+"\t "+"Nome: "+ nodo.nome + " indice osservabilità "+str(nodo.indice_oss)+ " finale "+str(nodo.final)+"\n"
    stampa += "Numero cammini generati: " + str(len(lista_cammini)) +"\n"
    for cammino in lista_cammini:
        stampa+="Nodo iniziale: "+str(cammino.nodo_iniziale.id) +"\t "+"Nome: "+ cammino.nome + "\t"+ "Nodo finale: "+str(cammino.nodo_finale.id)+"\t"+"Oss: "+cammino.oss+"\t"+"Ril: "+cammino.ril+"\n"
    if stampare==1:
        print(stampa)

    # Salvo i RisultatiTXT del metodo in file .txt e l'oggetto creato in file .json
    # Fine metodo, restituisco lo spazio creato
    formato_testo = ".txt"
    nome_file = "OL-" + rete.nome + "-" + stringa_nome_file
    with open("RisultatiTXT/" + nome_file + formato_testo, 'w', encoding='utf-8') as f:
        f.write(stampa)
    formato_json = ".json"
    risultato = SpazioComportamentaleOss(nodo_iniziale, lista_nodi, lista_cammini, rete.nome, stringa_nome_file)
    conv_json.CreaJSONdaRete("RisultatiJSON/" + nome_file + formato_json, risultato)

    return risultato

def potatura(lista_nodi,lista_cammini):
    # creiamo la lista di nodi non finali per poi potare
    global stampa
    stampa+="Nodi e cammini potati: \n"

    lista_nodi_potata = []
    finito = False
    lista_cammini_eliminati=[]
    lista_nodi_eliminati=[]

    while finito is False:
        finito = True
        for nodo in lista_nodi:
            for cammino in lista_cammini:
                if (nodo.nome == cammino.nodo_iniziale.nome and nodo.indice_oss == cammino.nodo_iniziale.indice_oss) or nodo.final is True:
                    if not any(nodo_pot for nodo_pot in lista_nodi_potata if nodo.nome==nodo_pot.nome and nodo_pot.indice_oss == nodo.indice_oss):
                        lista_nodi_potata.append(nodo)


        for nodo in lista_nodi:
            if not any(nodo_pot for nodo_pot in lista_nodi_potata if nodo.nome == nodo_pot.nome and nodo_pot.indice_oss == nodo.indice_oss):
                for cammino in lista_cammini:
                    if cammino.nodo_finale.nome == nodo.nome and cammino.nodo_finale.indice_oss == nodo.indice_oss:
                        lista_cammini.remove(cammino)
                        finito = False
                        lista_cammini_eliminati.append(cammino)
                        if not any(nodo_pot for nodo_pot in lista_nodi_eliminati if nodo.nome == nodo_pot.nome and nodo_pot.indice_oss == nodo.indice_oss):  # Se il nodo non è già presente nella lista dei nodi potati
                            lista_nodi_eliminati.append(nodo)


        lista_nodi=copy.deepcopy(lista_nodi_potata)
        lista_nodi_potata=[]



    stampa += "Numero nodi potati: " + str(len(lista_nodi_eliminati)) + "\n"
    for nodo in lista_nodi_eliminati:
        stampa+="Nome: "+ nodo.nome + " indice osservabilità "+str(nodo.indice_oss)+"\n"
    stampa += "\n"
    stampa += "Numero cammini potati: " + str(len(lista_cammini_eliminati)) + "\n"
    for cammino in lista_cammini_eliminati:
        stampa+="Nodo iniziale: "+str(cammino.nodo_iniziale.nome)+" indice oss:"+str(cammino.nodo_iniziale.indice_oss) +"\t "+"Nome transizione: "+ cammino.nome + "\t"+ "Nodo finale: "+str(cammino.nodo_finale.nome)+" indice oss:"+str(cammino.nodo_finale.indice_oss)+"\n"
    stampa+="\n"

    return lista_nodi, lista_cammini

def crea_nodo(nodo, transizione, id_FA, rete_lista_link): #aggiunti vediamo se utili al limite togliamo

    lista_nuovi_stati=copy.deepcopy(nodo.stati_FA)  #mi serve sapere i valori attuali
    lista_nuovi_link=copy.deepcopy(nodo.lista_link)


    if transizione.evento_in.evento.nome != "":
        link_funzione = transizione.evento_in.link
        evento_funzione = transizione.evento_in.evento
        indice_link = rete_lista_link.index(link_funzione)

        if lista_nuovi_link[indice_link].buffer != evento_funzione.nome:
            return None
        else:
            lista_nuovi_link[indice_link].buffer = ''

    funzioni_out = transizione.eventi_out.copy()
    for funzione_out in funzioni_out:
        link_funzione = funzione_out.link
        evento_funzione = funzione_out.evento

        indice_link = rete_lista_link.index(link_funzione)
        if lista_nuovi_link[indice_link].buffer != '':
            return None
        else:
            lista_nuovi_link[indice_link].buffer = evento_funzione.nome

    nuovo_indice=nodo.indice_oss
    if transizione.oss!='\u03b5':
        nuovo_indice+=1
    nuovi_stati = transizione.stato_f.nome
    lista_nuovi_stati[id_FA] = nuovi_stati

    return Nodo(lista_nuovi_stati,lista_nuovi_link,indice_oss=nuovo_indice)