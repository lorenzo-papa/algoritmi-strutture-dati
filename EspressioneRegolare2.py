from random import random, randint

from strutture_dati import *
import copy
import numpy as np
stampa=""
def EspressioneRegolare(spazioComportamentaleOss,stampare=0):

    #Preparazione degli oggetti che serviranno nel metodo
    lista_nodi=copy.deepcopy(spazioComportamentaleOss.lista_nodi)
    lista_cammini=copy.deepcopy(spazioComportamentaleOss.lista_cammini)
    nodi_finali=[]

    #Raccolgo i nodi di accettazione della rete
    for nodo in lista_nodi:
        if nodo.final == True:
            nodi_finali.append(nodo)

    #Se la rete non possiede nodi di accettazione interrompo
    if len(nodi_finali)==0:
        stampa = "La tua rete non contiene nodi di accettazione"
        if stampare == 1:
            print(stampa)
        return '\u03b5'

    #Se la rete contiene meno di due nodi o nessun cammino allora non è possibile calcolare l'espressione regolare su questa
    if len(lista_nodi) < 2 or len(lista_cammini) < 1 :
        stampa = "La tua rete contiene un solo nodo"
        if stampare == 1:
            print(stampa)
        return '\u03b5'

    #Se la rete contiene esattamente due nodi e un cammino posso trovare l'espressione regolare guardando quale dei nodi è finale e l'etichetta del cammino
    if len(lista_nodi) == 2 and len(lista_cammini) == 1:
        stampa = "La tua rete contiene un solo cammino"
        if stampare == 1:
            print(stampa)
        if lista_nodi[1].final == True:
            return lista_cammini[0].ril
        return '\u03b5'

    #Gestisco il caso di una rete con due nodi e due cammini che formano un loop tra i due nodi
    if len(lista_nodi) == 2 and len(lista_cammini) == 2 and lista_cammini[0].nodo_iniziale.id == lista_cammini[1].nodo_finale.id:
        #Se entrambi i nodi sono di accettazione
        if lista_nodi[0].final == True and lista_nodi[1].final == True:

            if lista_cammini[1].nodo_iniziale.id == lista_nodi[0].id:
                label_0 = gestioneLabelMetodo(lista_cammini[1], lista_cammini[0], lista_nodi[0], 0)
            else:
                label_0 = gestioneLabelMetodo(lista_cammini[0], lista_cammini[1], lista_nodi[0], 0)

            if lista_cammini[1].nodo_iniziale.id == lista_nodi[1].id:
                label_2 = gestioneLabelMetodo(lista_cammini[0], lista_cammini[1], lista_nodi[1], 1)
            else:
                label_2 = gestioneLabelMetodo(lista_cammini[1], lista_cammini[0], lista_nodi[1], 1)
            return riscrittura_label(label_0 +"|" +label_2)

        #Se solo il nodo iniziale è di accettazione
        elif lista_nodi[0].final == True:
            if lista_cammini[1].nodo_iniziale.id == lista_nodi[0].id:
                label_0 = gestioneLabelMetodo(lista_cammini[1], lista_cammini[0], lista_nodi[0], 0)
            else:
                label_0 = gestioneLabelMetodo(lista_cammini[0], lista_cammini[1], lista_nodi[0], 0)
            return label_0

        #Se solo il secondo nodo è di accettazione
        elif lista_nodi[1].final == True:
            if lista_cammini[1].nodo_iniziale.id == lista_nodi[0].id:
                label_0 = gestioneLabelMetodo(lista_cammini[1], lista_cammini[0], lista_nodi[1], 1)
            else:
                label_0 = gestioneLabelMetodo(lista_cammini[0], lista_cammini[1], lista_nodi[1], 1)
            return label_0
        #Se non ci sono nodi di accettazione
        else:
            return '\u03b5'

    #Rendo l'attributo final di tutti i nodi a false, creo un nuovo nodi finale e lo collego ai nodi di accettazione della rete
    for nodo in lista_nodi:
        if nodo.final == True:
            nodo.final=False

    id_nuovo=max(nodo.id for nodo in lista_nodi)+1
    nodo_finale=Nodo([],[],id=id_nuovo,final=True)
    lista_nodi.append(nodo_finale)
    for nodo in nodi_finali:
        lista_cammini.append(Cammino(nodo,nodo_finale))

    #elimina = False
    #Inizio corpo del metodo
    while len(lista_nodi)>2:
        nodo=lista_nodi[randint(0,len(lista_nodi)-1)]   #Prendo un nodo in maniera casuale tra quelli disponibili
        # Controllo che il nodo non sia di accettazione
        if nodo.final==False:
            cammini_entranti=[]
            cammini_uscenti=[]
            autotransizioni=[]

            #Calcolo per il nodo preso in considerazione i cammini entranti, uscenti, autotransizioni e nodi uscenti con la stessa destinazione
            for cammino in lista_cammini:
                if cammino.nodo_iniziale.id==nodo.id and cammino.nodo_finale.id==nodo.id:
                    autotransizioni.append(cammino)
                elif cammino.nodo_iniziale.id==nodo.id:
                    cammini_uscenti.append(cammino)
                elif cammino.nodo_finale.id==nodo.id:
                    cammini_entranti.append(cammino)
            cammini_uscenti_uguali=calcoloCamminiUguali(cammini_uscenti)

            #Se ho solo un cammino entrante e uno uscente allora unisco le due label e elimino il nodo
            if len(cammini_entranti)==1 and len(cammini_uscenti)==1 and len(autotransizioni)==0:
                nuovo_cammino = Cammino(cammini_entranti[0].nodo_iniziale, cammini_uscenti[0].nodo_finale, ril="")

                finale=gestioneLabelNOAutotrans(cammini_entranti[0],cammini_uscenti[0])
                nuovo_cammino.ril = finale

                lista_nodi.remove(nodo)
                if checkCammino(nuovo_cammino, lista_cammini) is True:
                    lista_cammini.append(nuovo_cammino)
                lista_cammini.remove(cammini_entranti[0])
                lista_cammini.remove(cammini_uscenti[0])

            #Gestisco il caso in cui ci siano due cammini paralleli uscenti dal nodo unendo le loro label in alternativa
            elif len(cammini_uscenti_uguali)>1:
                finale=''
                nodo_in=cammini_uscenti_uguali[0].nodo_iniziale
                #In caso i cammini paralleli fossero pipù di 2
                if len(cammini_uscenti_uguali) > 2:
                    # rimuovo i cammini dalla lista cammini per poi aggiungere quello risultante
                    for cammino_da_eliminare in cammini_uscenti_uguali:
                        lista_cammini.remove(cammino_da_eliminare)
                    #Salvo i nodi dei cammini paralleli
                    nodi_out = []
                    for cammino_out in cammini_uscenti_uguali:
                        if cammino_out.nodo_finale not in nodi_out:
                            nodi_out.append(cammino_out.nodo_finale)
                    nodi_out=removeNodiDoppi(nodi_out)

                    #per ogni nodo_out unisco i cammini che vanno in quel nodo
                    for nodo in nodi_out:
                        finale=""
                        for cammino_out in cammini_uscenti_uguali:
                            if nodo.id == cammino_out.nodo_finale.id:
                                finale += cammino_out.ril+'|'
                        finale = finale[:-1]
                        cammino_doppio = Cammino(nodo_in, nodo, ril=riscrittura_label(finale))
                        lista_cammini.append(cammino_doppio)
                #Se i cammini paralleli sono solamente 2
                else:
                    nodo_out = cammini_uscenti_uguali[0].nodo_finale
                    for cammino_da_eliminare in cammini_uscenti_uguali:
                        lista_cammini.remove(cammino_da_eliminare)
                    while len(cammini_uscenti_uguali)>0:
                        finale += '|' + cammini_uscenti_uguali.pop().ril
                    finale = finale[1:]
                    cammino_doppio=Cammino(nodo_in, nodo_out, ril=riscrittura_label(finale))
                    lista_cammini.append(cammino_doppio)
            #In caso di autotransizioni o caso generico
            else:
                #Se ci sono autotransizioni
                if len(autotransizioni)>0:
                    if nodo.final is False and nodo.id != lista_nodi[0].id:
                        for autotransizione in autotransizioni:
                            if autotransizione.ril == '\u03b5':
                                lista_cammini.remove(autotransizione)
                            else:
                                for cammino_in in cammini_entranti:
                                    for cammino_out in cammini_uscenti:
                                        finale=gestioneLabelAutotrans(cammino_in,autotransizione,cammino_out)
                                        nuovo_cammino = Cammino(cammino_in.nodo_iniziale,cammino_out.nodo_finale,ril=finale)
                                        if checkCammino(nuovo_cammino, lista_cammini) is True:
                                            lista_cammini.append(nuovo_cammino)
                                    lista_cammini.remove(cammino_in)
                                lista_cammini.remove(autotransizione)

                                for cammino_out_da_rimuovere in cammini_uscenti:
                                    lista_cammini.remove(cammino_out_da_rimuovere)

                                lista_nodi.remove(nodo)
                #Caso generale
                else:
                    if nodo.final is False and nodo.id != lista_nodi[0].id:
                        for cammino_in in cammini_entranti:
                            for cammino_out in cammini_uscenti:
                                finale=gestioneLabelNOAutotrans(cammino_in,cammino_out)

                                nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale, ril=finale)
                                if checkCammino(nuovo_cammino, lista_cammini) is True:
                                    lista_cammini.append(nuovo_cammino)
                            lista_cammini.remove(cammino_in)

                        for cammino_out_da_rimuovere in cammini_uscenti:
                            lista_cammini.remove(cammino_out_da_rimuovere)

                        lista_nodi.remove(nodo)
    #Fine While

    #Gestisco l'etichetta di output
    final_label_ril=""
    #In caso ci sia più di di un cammino allora sono cammini paralleli dal nodo iniziale al nodo finale
    if len(lista_cammini)>1:
        for cammino in lista_cammini:
            final_label_ril += '|'+ cammino.ril
        final_label_ril=final_label_ril[1:]
        final_label_ril=riscrittura_label(final_label_ril)
        stampa=final_label_ril
        if stampare==1:
            print(stampa)

        return final_label_ril

    #Se il cammino tra nodo iniziale e finale è unico
    elif len(lista_cammini)==1:
        final_label_ril = riscrittura_label(lista_cammini[0].ril)
        stampa=final_label_ril
        if stampare==1:
            print(stampa)
        return lista_cammini[0].ril
    else:
        return '\u03b5'



#Funzioni varie di utilità


#calcolo cammini uscenti uguali (da stesso e verso stesso nodo)
def calcoloCamminiUguali(camminiUscenti):
    camminiUscentiUguali=[]
    for x in range(len(camminiUscenti) - 2):
        for y in range(x,len(camminiUscenti)-1):
            if camminiUscenti[x].nodo_finale.id == camminiUscenti[y].nodo_finale.id and x != y:
                if camminiUscenti[x] not in camminiUscentiUguali:
                    camminiUscentiUguali.append(camminiUscenti[x])
                if camminiUscenti[y] not in camminiUscentiUguali:
                    camminiUscentiUguali.append(camminiUscenti[y])

    return camminiUscentiUguali

#rimuovo dal calcolo dei nodi di uscita dei cammini alternativi i nodi contati due volte
#TODO: vedi se si può fare direttamente da codice sopra, facendo cicli e controllando ID
def removeNodiDoppi(nodi_out):
    x = 0
    while x < len(nodi_out) - 1:
        y = x + 1
        while y < len(nodi_out):
            if nodi_out[x].id == nodi_out[y].id and x != y:
                nodi_out.remove(nodi_out[y])
            else:
                y = y + 1
        x = x + 1
    return nodi_out

#verifico se il cammino è già presente, altrimenti lo aggiungo alla lista
def checkCammino(nuovoCammino,listaCammini):
    for cammino in listaCammini:
        if cammino.nodo_iniziale.id == nuovoCammino.nodo_iniziale.id and cammino.nodo_finale.id == nuovoCammino.nodo_finale.id and cammino.ril == nuovoCammino.ril:
            return False
    return True

#Gestisco il caso in cui ci sia un ciclo in una rete con due nodi e due cammini in loop
def gestioneLabelMetodo(cammino_in,cammino_out,nodo,posizione):

    lista_cammino_precedente = cammino_in.ril.split("|")
    if cammino_out != '\u03b5':
        lista_cammino_seguente = cammino_out.ril.split("|")

    else:
        lista_cammino_seguente='\u03b5'
    lista_finale = []
    nodo_finale=False
    if posizione==1:
        for x in range(len(lista_cammino_precedente)):
            for y in range(len(lista_cammino_seguente)):
                if lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append(
                        lista_cammino_precedente[x] + "(" +lista_cammino_seguente[y]+lista_cammino_precedente[x]+")*")
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append('\u03b5')
                elif lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append(lista_cammino_precedente[x] + "(" + lista_cammino_precedente[x]  + ")"+ "*")
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append("(" + lista_cammino_seguente[y])  + ")" + "*"
            finale = ""
            for z in lista_finale:
                finale += z + "|"
            finale = finale[:-1]
    else:
        for x in range(len(lista_cammino_precedente)):
            for y in range(len(lista_cammino_seguente)):
                if lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append(
                       "(" +lista_cammino_precedente[x]+lista_cammino_seguente[y]+")*")
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append('\u03b5')
                elif lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append( "(" + lista_cammino_precedente[x]  + ")"+ "*")
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append("(" + lista_cammino_seguente[y])  + ")" + "*"
            finale = ""
            for z in lista_finale:
                finale += z + "|"
            finale = finale[:-1]
    return finale

#verifico label "duplicate" all'interno di cammini con alternative
def riscrittura_label(final):

    elementi_alternativi=final.split('|')
    x = 0
    while x < len(elementi_alternativi) - 1:
        y = x + 1
        while y < len(elementi_alternativi):
            if elementi_alternativi[x] == elementi_alternativi[y] and x != y:
                elementi_alternativi.pop(y)
            else:
                y = y + 1
        x = x + 1

    finale = ""
    for x in elementi_alternativi:
        finale += x + '|'
    finale = finale[:-1]
    return finale

#Gestisco le label in caso di autotransizione
def gestioneLabelAutotrans(cammino_in,autotransizione,cammino_out):
    lista_cammino_precedente = cammino_in.ril.split("|")
    lista_cammino_aut = autotransizione.ril.split("|")
    lista_cammino_seguente = cammino_out.ril.split("|")

    lista_finale = []
    for x in range(len(lista_cammino_precedente)):
        for z in range(len(lista_cammino_aut)):
            for y in range(len(lista_cammino_seguente)):
                if lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append(lista_cammino_precedente[x] + "(" + lista_cammino_aut[z] + ")"  + "*"+ lista_cammino_seguente[y])
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append("(" + lista_cammino_aut[z]  + ")"+ "*")
                elif lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append(lista_cammino_precedente[x] + "(" + lista_cammino_aut[z]  + ")"+ "*")
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append("(" + lista_cammino_aut[z]  + ")" + "*"+lista_cammino_seguente[y])
        finale = ""
        for z in lista_finale:
            finale += z + "|"
        finale = finale[:-1]
        return finale

#Gestisco le label in caso ci sia un cammino entrante e uno uscente
def gestioneLabelNOAutotrans(cammino_in,cammino_out):
    lista_cammino_precedente = cammino_in.ril.split("|")
    lista_cammino_seguente = cammino_out.ril.split("|")
    lista_finale = []
    for x in range(len(lista_cammino_precedente)):
        for y in range(len(lista_cammino_seguente)):
            if lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                lista_finale.append(lista_cammino_precedente[x] + lista_cammino_seguente[y])
            elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                lista_finale.append('\u03b5')
            elif lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                lista_finale.append(lista_cammino_precedente[x])
            elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                lista_finale.append(lista_cammino_seguente[y])
    finale = ""
    for z in lista_finale:
        finale += z + "|"
    finale = finale[:-1]
    return finale
