from random import random, randint
import copy
from strutture_dati import *

def EspressioniRegolari(spazioComportamentaleOss,stampare=0):
    stampa = ""

    #creazione automa
    lista_nodi = copy.deepcopy(spazioComportamentaleOss.lista_nodi)
    lista_cammini = copy.deepcopy(spazioComportamentaleOss.lista_cammini)
    nodi_finali=[]

    #Raccolgo i nodi finali
    for nodo in lista_nodi:
        if nodo.final == True:
            nodi_finali.append(nodo)  # stati di terminazione

    #Controllo se nella rete son presenti nodi di accettazione
    if len(nodi_finali)==0:
        stampa += "La tua rete non contiene nodi di accettazione"
        if stampare == 1:
            print(stampa)
        return [Cammino(None,None,ril='\u03b5')]

    #Gestisco il caso in cui ci siano meno di 2 nodi o nessun cammino
    if len(lista_nodi) < 2 or len(lista_cammini) < 1 :
        stampa+="La tua rete contiene un solo nodo"
        nodo_temp=Nodo([],[], id=1000)
        if stampare==1:
            print(stampa)
        return [Cammino(nodo_temp,nodo_temp,nodo_accettazione_raggiunto=lista_nodi[0].id)]

    #Gestisco il caso in cui la rete ha due nodi e due cammini che formano un loop
    if len(lista_nodi) == 2 and len(lista_cammini) ==2 and lista_cammini[0].nodo_iniziale.id==lista_cammini[1].nodo_finale.id:
        if lista_nodi[0].final==True and lista_nodi[1].final==True:

            if lista_cammini[1].nodo_iniziale.id==lista_nodi[0].id:
                label_0=gestioneLabelCiclo(lista_cammini[1],lista_cammini[0],lista_nodi[0],0)
            else:
                label_0=gestioneLabelCiclo(lista_cammini[0],lista_cammini[1],lista_nodi[0],0)

            nodo_temp = Nodo([], [], id=1000)
            cammino_nuovo=Cammino(nodo_temp,nodo_temp,ril=label_0,nodo_accettazione_raggiunto=lista_nodi[0].id)
            if lista_cammini[1].nodo_iniziale.id==lista_nodi[1].id:
                label_2=gestioneLabelCiclo(lista_cammini[0],lista_cammini[1],lista_nodi[1],1)
            else:
                label_2=gestioneLabelCiclo(lista_cammini[1],lista_cammini[0],lista_nodi[1],1)
            cammino_nuovo2=Cammino(nodo_temp,nodo_temp,ril=label_2,nodo_accettazione_raggiunto=lista_nodi[1].id)
            stampa += "{" + cammino_nuovo.ril + "}" + "_" + str(cammino_nuovo.nodo_accettazione_raggiunto) + "\n"
            stampa += "{" + cammino_nuovo2.ril + "}" + "_" + str(cammino_nuovo2.nodo_accettazione_raggiunto) + "\n"
            if stampare == 1:
                print(stampa)
            return[cammino_nuovo,cammino_nuovo2]
        elif lista_nodi[0].final==True:
            if lista_cammini[1].nodo_iniziale.id==lista_nodi[0].id:
                label_0 = gestioneLabelCiclo(lista_cammini[1], lista_cammini[0], lista_nodi[0],0)
            else:
                label_0 = gestioneLabelCiclo(lista_cammini[0], lista_cammini[1], lista_nodi[0],0)

            nodo_temp = Nodo([], [], id=1000)
            cammino_nuovo = Cammino(nodo_temp, nodo_temp, ril=label_0, nodo_accettazione_raggiunto=lista_nodi[0].id)
            stampa += "{" + cammino_nuovo.ril + "}" + "_" + str(cammino_nuovo.nodo_accettazione_raggiunto) + "\n"
            if stampare == 1:
                print(stampa)
            return [cammino_nuovo]
        elif lista_nodi[1].final==True:
            if lista_cammini[1].nodo_iniziale.id==lista_nodi[0].id:
                label_0 = gestioneLabelCiclo(lista_cammini[1], lista_cammini[0], lista_nodi[1],1)
            else:
                label_0 = gestioneLabelCiclo(lista_cammini[0], lista_cammini[1], lista_nodi[1],1)

            nodo_temp = Nodo([], [], id=1000)
            cammino_nuovo = Cammino(nodo_temp, nodo_temp, ril=label_0, nodo_accettazione_raggiunto=lista_nodi[1].id)
            stampa += "{" + cammino_nuovo.ril + "}" + "_" + str(cammino_nuovo.nodo_accettazione_raggiunto) + "\n"
            if stampare == 1:
                print(stampa)
            return [cammino_nuovo]

    #Se la rete comrprende solo due nodi e un cammino
    if len(lista_nodi) == 2 and len(lista_cammini) == 1:
        stampa += "La tua rete contiene un solo cammino \n"
        if lista_nodi[0].final==True and lista_nodi[1].final==True:
            cammino_nuovo = lista_cammini[0]
            cammino_nuovo.nodo_accettazione_raggiunto = lista_nodi[1].id
            nodo_temp = Nodo([], [], id=1000)
            cammino_nuovo2 = Cammino(nodo_temp, nodo_temp)
            cammino_nuovo2.nodo_accettazione_raggiunto = lista_nodi[0].id
            stampa += "{" + cammino_nuovo.ril + "}" + "_" + str(cammino_nuovo.nodo_accettazione_raggiunto) + "\n"
            stampa += "{" + cammino_nuovo2.ril + "}" + "_" + str(cammino_nuovo2.nodo_accettazione_raggiunto) + "\n"
            if stampare == 1:
                print(stampa)
            return [cammino_nuovo,cammino_nuovo2]

        elif lista_nodi[1].final==True:
            cammino_nuovo = lista_cammini[0]
            cammino_nuovo.nodo_accettazione_raggiunto=lista_nodi[1].id
            stampa += "{" + cammino_nuovo.ril + "}" + "_" + str(cammino_nuovo.nodo_accettazione_raggiunto) + "\t"
            if stampare == 1:
                print(stampa)
            return [cammino_nuovo]
        elif lista_nodi[0].final==True:
            nodo_temp = Nodo([], [], id=1000)
            cammino_nuovo=Cammino(nodo_temp,nodo_temp)
            cammino_nuovo.nodo_accettazione_raggiunto = lista_nodi[0].id
            stampa += "{" + cammino_nuovo.ril + "}" + "_" + str(cammino_nuovo.nodo_accettazione_raggiunto) + "\t"
            if stampare == 1:
                print(stampa)
            return [cammino_nuovo]

    #Creo un nuovo nodo iniziale e lo collego al cammino iniziale
    for cammino in lista_cammini:
        if cammino.nodo_finale.id == lista_nodi[0].id:
            id_nuovo = min(nodo.id for nodo in lista_nodi) - 1
            nodo_iniziale = Nodo([], [], id=id_nuovo, final=False)
            lista_nodi.insert(0,nodo_iniziale)
            lista_cammini.insert(Cammino(nodo_iniziale,lista_nodi[1]))

    #Cambio lo stato final di tutti i nodi, in quanto l'unico nodo finale sarà quello aggiunto successivamente
    for nodo in lista_nodi:
        if nodo.final == True:
            nodo.final=False

    #Aggiungo nuovo nodo finale
    id_nuovo_finale=max(nodo.id for nodo in lista_nodi)+1
    nodo_finale=Nodo([],[],id=id_nuovo_finale,final=True)
    lista_nodi.append(nodo_finale)


    for nodo in nodi_finali:
        lista_cammini.append(Cammino(nodo,nodo_finale))


    elimina = False
    while len(lista_nodi) > 2:
        #Prendo un nodo random
        nodo = lista_nodi[randint(1, len(lista_nodi) - 2)]

        #Calcolo i cammini entranti, uscenti, autotransizioni e uscenti uguali
        if nodo.final == False:
            cammini_entranti = []
            cammini_uscenti = []
            autotransizioni = []
            for cammino in lista_cammini:
                if cammino.nodo_iniziale.id == nodo.id and cammino.nodo_finale.id == nodo.id:
                    autotransizioni.append(cammino)
                elif cammino.nodo_iniziale.id == nodo.id:
                    cammini_uscenti.append(cammino)
                elif cammino.nodo_finale.id == nodo.id:
                    cammini_entranti.append(cammino)
            cammini_uscenti_uguali = calcoloCamminiUguali(cammini_uscenti)
            (cammini_paralleli_no_label,cammini_paralleli_con_label)=checkPediceCamminiParalleli(cammini_uscenti_uguali)

            #Metodo per nodi con solo un cammino in entrata e uno in uscita, cammini senza etichietta del nodo di accettazione
            if len(cammini_entranti) == 1 and len(cammini_uscenti) == 1 and len(autotransizioni) == 0 and cammini_uscenti[0].nodo_accettazione_raggiunto==None:

                nuovo_cammino = Cammino(cammini_entranti[0].nodo_iniziale, cammini_uscenti[0].nodo_finale, ril="")
                finale=gestioneLabelNOAutotrans(cammini_entranti[0],cammini_uscenti[0])
                nuovo_cammino.ril = finale

                if nodo not in nodi_finali and cammini_uscenti[0].nodo_finale.final is False:
                    pass
                else:
                    nuovo_cammino.nodo_accettazione_raggiunto = nodo.id
                lista_nodi.remove(nodo)

                if checkCammino(nuovo_cammino, lista_cammini) is True:
                    lista_cammini.append(nuovo_cammino)
                lista_cammini.remove(cammini_entranti[0])
                lista_cammini.remove(cammini_uscenti[0])

            #Metodo per nodi con solo un cammino in entrata e uno in uscita, cammini con etichietta del nodo di accettazione
            elif len(cammini_entranti) == 1 and len(cammini_uscenti) == 1 and len(autotransizioni) == 0 and cammini_uscenti[0].nodo_accettazione_raggiunto!= None:
                nuovo_cammino = Cammino(cammini_entranti[0].nodo_iniziale, cammini_uscenti[0].nodo_finale, ril="")
                finale=gestioneLabelNOAutotrans(cammini_entranti[0],cammini_uscenti[0])
                nuovo_cammino.ril = finale
                nuovo_cammino.nodo_accettazione_raggiunto = cammini_uscenti[0].nodo_accettazione_raggiunto
                lista_nodi.remove(nodo)
                if checkCammino(nuovo_cammino, lista_cammini) is True:
                    lista_cammini.append(nuovo_cammino)
                lista_cammini.remove(cammini_entranti[0])
                lista_cammini.remove(cammini_uscenti[0])

            #Metodo per gestire cammini paralleli uscenti da un nodo senza etichetta del nodo di accettazione
            elif len(cammini_paralleli_no_label)>1:

                finale = ''
                nodo_in = cammini_paralleli_no_label[0].nodo_iniziale
                #Se i cammini paralleli son più di due(anche coppie dirette verso nodi differenti)
                if len(cammini_paralleli_no_label) > 2:
                    for cammino_da_eliminare in cammini_paralleli_no_label:
                        lista_cammini.remove(cammino_da_eliminare)

                    nodi_out = []
                    for cammino_out in cammini_paralleli_no_label:
                        if cammino_out.nodo_finale not in nodi_out:  # sarà da fare sugli id  (mettere secondo for)
                            nodi_out.append(cammino_out.nodo_finale)
                    nodi_out = removeNodiDoppi(nodi_out)

                    for nodo in nodi_out:
                        finale = ""
                        for cammino_out in cammini_paralleli_no_label:
                            if nodo.id == cammino_out.nodo_finale.id:
                                finale += cammino_out.ril + '|'
                        finale = finale[:-1]
                        cammino_doppio = Cammino(nodo_in, nodo, ril=riscrittura_label(finale))
                        lista_cammini.append(cammino_doppio)
                #Se c'è solo una coppia di cammini paralleli
                else:
                    nodo_out = cammini_uscenti_uguali[0].nodo_finale
                    for cammino_da_eliminare in cammini_paralleli_no_label:
                        lista_cammini.remove(cammino_da_eliminare)

                    while len(cammini_paralleli_no_label)>0:
                        finale += '|' + cammini_paralleli_no_label.pop().ril
                    finale = finale[1:]
                    cammino_doppio = Cammino(nodo_in, nodo_out, ril=riscrittura_label(finale))
                    lista_cammini.append(cammino_doppio)

            #Metodo per gestire cammini paralleli uscenti da un nodo con etichietta del nodo di accettazione
            elif len(cammini_paralleli_con_label)>1:

                finale = ''
                nodo_in = cammini_paralleli_con_label[0].nodo_iniziale

                if len(cammini_paralleli_con_label) > 2:
                    for cammino_da_eliminare in cammini_paralleli_con_label:
                        lista_cammini.remove(cammino_da_eliminare)

                    nodi_out = []
                    label_out = []
                    for cammino_out in cammini_paralleli_con_label:
                        if cammino_out.nodo_finale not in nodi_out:
                            nodi_out.append(cammino_out.nodo_finale)
                        if cammino_out.nodo_accettazione_raggiunto not in label_out:
                            label_out.append(cammino_out.nodo_accettazione_raggiunto)
                    nodi_out = removeNodiDoppi(nodi_out)  # dovrebbe rimuovere duplicati
                    label_out = removeLabelDoppie(label_out)

                    for nodo in nodi_out:
                        for label in label_out:
                            finale = ""
                            for cammino_out in cammini_paralleli_con_label:
                                if nodo.id == cammino_out.nodo_finale.id and label == cammino_out.nodo_accettazione_raggiunto:

                                    finale += cammino_out.ril + '|'
                            finale = finale[:-1]
                            if finale != "":
                                cammino_doppio = Cammino(nodo_in, nodo, ril=riscrittura_label(finale))
                                cammino_doppio.nodo_accettazione_raggiunto=label

                            if checkCammino(cammino_doppio, lista_cammini):
                                lista_cammini.append(cammino_doppio)  # cammino_da_aggiungere
                else:
                    nodo_out = cammini_paralleli_con_label[0].nodo_finale
                    label_act=cammini_paralleli_con_label[0].nodo_accettazione_raggiunto
                    for cammino_da_eliminare in cammini_paralleli_con_label:
                        lista_cammini.remove(cammino_da_eliminare)

                    while len(cammini_paralleli_con_label) > 0:
                        finale += '|' + cammini_paralleli_con_label.pop().ril
                    finale = finale[1:]
                    cammino_doppio = Cammino(nodo_in, nodo_out, ril=riscrittura_label(finale))
                    cammino_doppio.nodo_accettazione_raggiunto=label_act

                    if checkCammino(cammino_doppio,lista_cammini):
                        lista_cammini.append(cammino_doppio)  # cammino_da_aggiungere


            else:
                #todo se c'è autotransizone

                if len(autotransizioni) > 0:

                    if nodo.final is False and nodo.id != lista_nodi[0].id:
                        for autotransizione in autotransizioni:
                            if autotransizione.ril == '\u03b5':
                                lista_cammini.remove(autotransizione)
                            else:
                                for cammino_in in cammini_entranti:
                                    for cammino_out in cammini_uscenti:


                                        if nodo in nodi_finali and cammino_out.nodo_finale.final:
                                            finale=gestioneLabelAutotrans(cammino_in,autotransizione,'\u03b5')
                                            nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_in.nodo_finale, ril=finale)
                                            nuovo_cammino.nodo_accettazione_raggiunto = nodo.id
                                            if checkCammino(nuovo_cammino, lista_cammini) is True:
                                                lista_cammini.append(nuovo_cammino)

                                            finale2 = gestioneLabelAutotrans(cammino_in, autotransizione, cammino_out)
                                            nuovo_cammino2 = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale, ril=finale2)
                                            nuovo_cammino2.nodo_accettazione_raggiunto = cammino_out.nodo_accettazione_raggiunto
                                            if checkCammino(nuovo_cammino2, lista_cammini) is True:
                                                lista_cammini.append(nuovo_cammino2)

                                        elif cammino_out.nodo_accettazione_raggiunto is not None:
                                            finale = gestioneLabelAutotrans(cammino_in, autotransizione, cammino_out)
                                            nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale,ril=finale)
                                            nuovo_cammino.nodo_accettazione_raggiunto = cammino_out.nodo_accettazione_raggiunto
                                            if checkCammino(nuovo_cammino, lista_cammini) is True:
                                                lista_cammini.append(nuovo_cammino)
                                        else:
                                            finale = gestioneLabelAutotrans(cammino_in, autotransizione, cammino_out)
                                            nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale,ril=finale)
                                            if checkCammino(nuovo_cammino, lista_cammini) is True:
                                                lista_cammini.append(nuovo_cammino)

                                    lista_cammini.remove(cammino_in)
                                lista_cammini.remove(autotransizione)
                                for cammino_out_da_rimuovere in cammini_uscenti:
                                    lista_cammini.remove(cammino_out_da_rimuovere)

                                lista_nodi.remove(nodo)
                else:
                    # todo se non c'è l'autotransizione

                    for cammino_in in cammini_entranti:
                        for cammino_out in cammini_uscenti:

                            if nodo in nodi_finali and cammino_out.nodo_finale.final:

                                finale = gestioneLabelNOAutotrans(cammino_in, '\u03b5')
                                nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_in.nodo_finale,
                                                        ril=finale)
                                nuovo_cammino.nodo_accettazione_raggiunto = nodo.id
                                if checkCammino(nuovo_cammino, lista_cammini) is True:
                                    elimina = True
                                    lista_cammini.append(nuovo_cammino)

                                finale2 = gestioneLabelNOAutotrans(cammino_in, cammino_out)
                                nuovo_cammino2 = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale,
                                                        ril=finale2)
                                nuovo_cammino2.nodo_accettazione_raggiunto = cammino_out.nodo_accettazione_raggiunto
                                if checkCammino(nuovo_cammino2, lista_cammini) is True:
                                    elimina = True
                                    lista_cammini.append(nuovo_cammino2)

                            elif cammino_out.nodo_accettazione_raggiunto is not None:

                                finale = gestioneLabelNOAutotrans(cammino_in, cammino_out)
                                nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale,
                                                        ril=finale)
                                nuovo_cammino.nodo_accettazione_raggiunto = cammino_out.nodo_accettazione_raggiunto
                                if checkCammino(nuovo_cammino, lista_cammini) is True:
                                    elimina = True
                                    lista_cammini.append(nuovo_cammino)
                            #todo elif in cui nodo di arrivo è nodo finale
                            elif cammino_out.nodo_finale.final is True:
                                finale = gestioneLabelNOAutotrans(cammino_in, cammino_out)
                                nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale,
                                                        ril=finale)
                                nuovo_cammino.nodo_accettazione_raggiunto = nodo.id
                                if checkCammino(nuovo_cammino, lista_cammini) is True:
                                    elimina = True
                                    lista_cammini.append(nuovo_cammino)
                            else:

                                finale = gestioneLabelNOAutotrans(cammino_in, cammino_out)
                                nuovo_cammino = Cammino(cammino_in.nodo_iniziale, cammino_out.nodo_finale,
                                                        ril=finale)
                                if checkCammino(nuovo_cammino, lista_cammini) is True:
                                    elimina=True
                                    lista_cammini.append(nuovo_cammino)
                        if cammino_in.nodo_accettazione_raggiunto==None:
                            lista_cammini.remove(cammino_in)
                    for cammino_out_da_rimuovere in cammini_uscenti:
                        lista_cammini.remove(cammino_out_da_rimuovere)

                    if elimina is True:
                        lista_nodi.remove(nodo)


    #todo STAMPA DELLE TRANSIZIONI FINALI
    lista_finale_cammini = []
    for nodo in nodi_finali:
        presente = False
        for cammino in lista_cammini:
            if cammino.nodo_accettazione_raggiunto == nodo.id:
                presente = True
        if presente == False:
            cammino_finale = Cammino(lista_nodi[0], nodo, ril='\u03b5', nodo_accettazione_raggiunto=nodo.id)
            lista_finale_cammini.append(cammino_finale)
            nodi_finali.remove(nodo)

    for nodo in nodi_finali:
        finale=""
        for cammino in lista_cammini:
            if cammino.nodo_accettazione_raggiunto==nodo.id:
                finale += cammino.ril + '|'
        finale = finale[:-1]
        cammino_finale=Cammino(lista_nodi[0],nodo,ril=riscrittura_label(finale),nodo_accettazione_raggiunto=nodo.id)
        lista_finale_cammini.append(cammino_finale)

    final_label=""
    for cammino in lista_finale_cammini:
        if cammino.nodo_accettazione_raggiunto is not None:
            final_label+="{"+cammino.ril+"}"+"_"+str(cammino.nodo_accettazione_raggiunto)+"\t"

    stampa=final_label
    if stampare==1:
        print(stampa)
    return lista_finale_cammini


##################################################################################################################

#todo FUNZIONI DI UTILITA' VARIE
#calcolo cammini uscenti uguali (da stesso e verso stesso nodo)
def calcoloCamminiUguali(camminiUscenti):
    camminiUscentiUguali=[]
    for x in range(len(camminiUscenti) - 1):
        for y in range(1,len(camminiUscenti)):
            if camminiUscenti[x].nodo_finale.id == camminiUscenti[y].nodo_finale.id and x != y:
                if camminiUscenti[x] not in camminiUscentiUguali:
                    camminiUscentiUguali.append(camminiUscenti[x])
                if camminiUscenti[y] not in camminiUscentiUguali:
                    camminiUscentiUguali.append(camminiUscenti[y])

    return camminiUscentiUguali


def checkPediceCamminiParalleli(cammini_uscenti_uguali):
    cammini_senza_pedice=[]
    cammini_con_pedice=[]

    for x in range(len(cammini_uscenti_uguali) - 2):
        for y in range(x,len(cammini_uscenti_uguali) - 1):
            if cammini_uscenti_uguali[x].nodo_finale.id == cammini_uscenti_uguali[y].nodo_finale.id and x != y:
                if cammini_uscenti_uguali[x].nodo_accettazione_raggiunto is None and cammini_uscenti_uguali[y].nodo_accettazione_raggiunto is None:
                    if cammini_uscenti_uguali[x] not in cammini_senza_pedice:
                        cammini_senza_pedice.append(cammini_uscenti_uguali[x])
                    if cammini_uscenti_uguali[y] not in cammini_senza_pedice:
                        cammini_senza_pedice.append(cammini_uscenti_uguali[y])
                #not None aggiunto per sicurezza (perchè anche due None sono uguali fra loro)
                elif cammini_uscenti_uguali[x].nodo_accettazione_raggiunto == cammini_uscenti_uguali[y].nodo_accettazione_raggiunto and cammini_uscenti_uguali[x].nodo_accettazione_raggiunto is not None:
                    if cammini_uscenti_uguali[x] not in cammini_con_pedice:
                        cammini_con_pedice.append(cammini_uscenti_uguali[x])
                    if cammini_uscenti_uguali[y] not in cammini_con_pedice:
                        cammini_con_pedice.append(cammini_uscenti_uguali[y])

    return (cammini_senza_pedice,cammini_con_pedice)#(paralleli_no_pedice,cammini_senza_pedice,paralleli_con_pedice,cammini_con_pedice)




#verifico se il cammino è già presente, altrimenti lo aggiungo alla lista
def checkCammino(nuovoCammino,listaCammini):
    for cammino in listaCammini:
        if cammino.nodo_iniziale.id == nuovoCammino.nodo_iniziale.id and cammino.nodo_finale.id == nuovoCammino.nodo_finale.id and cammino.ril == nuovoCammino.ril:
            if nuovoCammino.nodo_accettazione_raggiunto==cammino.nodo_accettazione_raggiunto:
                return False
    return True

#rimuovo dal calcolo dei nodi di uscita dei cammini alternativi i nodi contati due volte
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

def removeLabelDoppie(label_out):
    x = 0
    while x < len(label_out) - 1:
        y = x + 1
        while y < len(label_out):
            if label_out[x] == label_out[y] and x != y:
                label_out.remove(label_out[y])
            else:
                y = y + 1
        x = x + 1
    return label_out

#verifico label "duplicate" all'interno di cammini con alternative
def riscrittura_label(final):
    elementi_alternativi=final.split('|') #.ril
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

def gestioneLabelCiclo(cammino_in,cammino_out,nodo,posizione):

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

def gestioneLabelAutotrans(cammino_in,autotransizione,cammino_out):
    lista_cammino_precedente = cammino_in.ril.split("|")
    lista_cammino_aut = autotransizione.ril.split("|")
    if cammino_out != '\u03b5':
        lista_cammino_seguente = cammino_out.ril.split("|")
    else:
        lista_cammino_seguente='\u03b5'

    lista_finale = []
    for x in range(len(lista_cammino_precedente)):
        for z in range(len(lista_cammino_aut)):
            for y in range(len(lista_cammino_seguente)):
                if lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append(lista_cammino_precedente[x] + "(" + lista_cammino_aut[z] + "*" + ")" + lista_cammino_seguente[y])
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append("(" + lista_cammino_aut[z] + "*" + ")")
                elif lista_cammino_precedente[x] != '\u03b5' and lista_cammino_seguente[y] == '\u03b5':
                    lista_finale.append(lista_cammino_precedente[x] + "(" + lista_cammino_aut[z] + "*" + ")")
                elif lista_cammino_precedente[x] == '\u03b5' and lista_cammino_seguente[y] != '\u03b5':
                    lista_finale.append("(" + lista_cammino_aut[z] + "*" + ")" +lista_cammino_seguente[y])
        finale = ""
        for z in lista_finale:
            finale += z + "|"
        finale = finale[:-1]
        return finale

def gestioneLabelNOAutotrans(cammino_in,cammino_out):

    lista_cammino_precedente = cammino_in.ril.split("|")
    if cammino_out!='\u03b5':
        lista_cammino_seguente = cammino_out.ril.split("|")
    else:
        lista_cammino_seguente='\u03b5'

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