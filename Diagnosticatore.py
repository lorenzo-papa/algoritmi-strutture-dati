import strutture_dati
from strutture_dati import *
import EspressioneRegolare2 as er
import EspressioniRegolari as eri
import copy
import CreaReteJSON as conv_json

def spazio_chiusure(spazio_comportamentale, stampare=0):
    stampa = ""

    stampa += "Spazio delle chiusure relativo allo spazio comportamentale della rete "+spazio_comportamentale.nome_rete+"\n\n"
    lista_nodi = copy.deepcopy(spazio_comportamentale.lista_nodi)

    #Salvo i nodi di accettazione che mi serviranno nel metodo Diagnosticatore
    nodi_finali = []
    for nodo in lista_nodi:
        if nodo.final == True:
            nodi_finali.append(nodo)

    #Inizializzo le variabili che mi serviranno
    nodo_iniziale = spazio_comportamentale.nodo_iniziale
    lista_cammini = copy.deepcopy(spazio_comportamentale.lista_cammini)
    lista_cammini_chiusure = []
    lista_chiusure = []

    #Creo la chiusura del nodo iniziale
    chiusura = ricava_chiusura(nodo_iniziale, spazio_comportamentale, 0,nodi_finali)
    lista_chiusure.append(chiusura)

    id = 1
    #Creo tutte le chiusure della rete
    for cammino in lista_cammini:
        if cammino.oss != '\u03b5':
            chiusura = ricava_chiusura(cammino.nodo_finale, spazio_comportamentale, id, nodi_finali)

            #Verifico che non esista già una chiusura identica e se non esiste la aggiungo a lista chiusure
            aggiungi = True
            for chiusura_2 in lista_chiusure:
                count = 0
                if len(chiusura.lista_nodi) == len(chiusura_2.lista_nodi):#Controllo se la cardinalità degli elementi è uguale
                    for i in range(len(chiusura.lista_nodi)):
                        if chiusura.lista_nodi[i].id == chiusura_2.lista_nodi[i].id:#Verifico se i nodi son nella stessa posizione e in caso incremento il contatore
                            count += 1
                if count == len(chiusura.lista_nodi):#Se il contatore è uguale alla lunghezza della lista nodi allora tutti i nodi delle due chiusure sono uguali e quindi la chiusura è già presente nella lista
                    aggiungi = False
                    cammino.chiusura_finale = chiusura_2
                    lista_cammini_chiusure.append(cammino) #Aggiungo il cammino con chiusura finale uguale a quella già esistente nella rete
            if aggiungi == True: #se non esiste già nella lista aggiungo la nnuova chiusura alla lista e assegno al cammino questa chiusura come chiusura finale
                id += 1
                lista_chiusure.append(chiusura)
                cammino.chiusura_finale = chiusura
                lista_cammini_chiusure.append(cammino)

    lista_cammini_finale=[]

    #Assegno ad ogni cammino la chiusura di partenza e aggiungo i cammini ad una nuova lista
    for cammino in lista_cammini_chiusure:
        for chiusura in lista_chiusure:
            for nodo in chiusura.lista_nodi:
                if cammino.nodo_iniziale.id==nodo.id:
                    cammino_da_aggiungere=copy.deepcopy(cammino)
                    cammino_da_aggiungere.chiusura_iniziale=chiusura
                    lista_cammini_finale.append(cammino_da_aggiungere)

    #Gestisco la stampa di output
    stampa += "Chiusure totali:" + "\t" + str(len(lista_chiusure)) + "\n"
    for chiusura in lista_chiusure:
        stampa += "ID chiusura: " + str(chiusura.id) + ",\t nodi in chiusura: "
        for nodo in chiusura.lista_nodi:
            stampa += str(nodo.id) + ", "
        stampa = stampa[:-2]

        stampa+="\n"
    stampa+="\n"
    stampa += "Cammini totali:" + "\t" + str(len(lista_cammini_finale)) + "\n"

    for cammino in lista_cammini_finale:
        stampa += "Cammino: Chiusura di partenza: " + str(cammino.chiusura_iniziale.id) + ", Chiusura finale: " + str(
            cammino.chiusura_finale.id) + ", Nodo iniziale: " + str(cammino.nodo_iniziale.id) + ", Nodo finale: " + str(
            cammino.nodo_finale.id) + ", Etichetta osservabilità " + cammino.oss+"\n"
    if stampare == 1:
        print(stampa)

    formato_testo = ".txt"
    formato_json = ".json"
    nome_file = "Chiusure-" + spazio_comportamentale.nome_rete
    with open("RisultatiTXT/" + nome_file + formato_testo, 'w', encoding='utf-8') as f:
        f.write(stampa)
    risultato = SpazioChiusure(lista_chiusure, lista_cammini_finale, nodi_finali, spazio_comportamentale.nome_rete)
    conv_json.CreaJSONdaRete("RisultatiJSON/" + nome_file + formato_json, risultato)
    return risultato

    return SpazioChiusure(lista_chiusure,lista_cammini_finale,nodi_finali,spazio_comportamentale.nome_rete)


def diagnosticatore(spazio_chiusure, stampare=0):
    stampa = ""


    stampa += "Diagnosticatore dello spazio delle chiusure relativo allo spazio comportamentale della rete "+spazio_chiusure.nome_rete+"\n\n"

    #Inizializzo i dati che mi servono
    lista_chiusure = copy.deepcopy(spazio_chiusure.lista_chiusure)
    lista_cammini_diagnosi=copy.deepcopy(spazio_chiusure.lista_cammini)
    nodi_finali = copy.deepcopy(spazio_chiusure.nodi_finali)

    #Creo la diagnosi di ogni chiusura
    for chiusura in lista_chiusure:
        diagnosi=er.EspressioneRegolare(chiusura)
        chiusura.diagnosi_relativa=diagnosi

    #Operazioni di stampa per output e assegno l'attributo final=True a ogni nodo della chiusura per il quale esiste un cammino uscente, fatto per far funzionare espressioni regolari per calcolo etichetta cammini
    stampa+="Chiusure totali:"+"\t"+str(len(lista_chiusure))+"\n"
    for chiusura in lista_chiusure:
        stampa+="ID chiusura: "+ str(chiusura.id)+",\t nodi in chiusura: "

        for nodo in chiusura.lista_nodi:
            stampa+=str(nodo.id)+", "
            nodo.final=False
            for nodo2 in chiusura.lista_nodi_uscenti:
                if nodo2.id==nodo.id:
                    nodo.final=True
        stampa=stampa[:-2]
        chiusura_corretta=correzione_label_chiusura(chiusura.diagnosi_relativa)
        stampa+="\t"+"Diagnosi chiusura: "+ chiusura_corretta +"\n"
    stampa+="\n"

    for cammino in lista_cammini_diagnosi:
        for chiusura in lista_chiusure:
            if cammino.chiusura_iniziale.id==chiusura.id:
                cammino.chiusura_iniziale=chiusura
            if cammino.chiusura_finale.id==chiusura.id:
                cammino.chiusura_finale=chiusura

    #Richiama espressioni regolari su ogni chiusura iniziale del cammino per decretare la sua decorazione
    for cammino in lista_cammini_diagnosi:
        lista_cammini_espressioni_regolari=eri.EspressioniRegolari(cammino.chiusura_iniziale)
        for cammino_exp in lista_cammini_espressioni_regolari:
            if cammino_exp.nodo_accettazione_raggiunto==cammino.nodo_iniziale.id:
                cammino.etichetta_diagnosi=cammino_exp.ril

    #Operazioni di stampa per l'output
    stampa+="Cammini totali:"+"\t"+str(len(lista_cammini_diagnosi))+"\n"

    for cammino in lista_cammini_diagnosi:
        stampa += "Cammino: Chiusura di partenza: " + str(cammino.chiusura_iniziale.id) + ", Chiusura finale: " + str(
            cammino.chiusura_finale.id) + ", Nodo iniziale: " + str(cammino.nodo_iniziale.id) + ", Nodo finale: " + str(
            cammino.nodo_finale.id) + ", Etichetta diagnosi " + cammino.etichetta_diagnosi + ", Etichetta osservabilità " + cammino.oss + "\n"
    if stampare==1:
        print(stampa)

    #Riassegno a ogni chiusura i nodi finali corretti
    for chiusura in lista_chiusure:
        for nodo in chiusura.lista_nodi:
            for nodo2 in nodi_finali:
                if nodo.id==nodo2.id:
                    nodo.final=True
                    chiusura.final=True
                else:
                    nodo.final=False


    for chiusura in lista_chiusure:
        for nodo in chiusura.lista_nodi:
            for nodo2 in nodi_finali:
                if nodo.id==nodo2.id:
                    nodo.final=True
                else:
                    nodo.final=False

    for cammino in lista_cammini_diagnosi:
        for chiusura in lista_chiusure:
            if cammino.chiusura_iniziale.id==chiusura.id:
                cammino.chiusura_iniziale=chiusura
            if cammino.chiusura_finale.id==chiusura.id:
                cammino.chiusura_finale=chiusura

    formato_testo = ".txt"
    formato_json = ".json"

    nome_file = "Diagnosticatore-" + spazio_chiusure.nome_rete
    with open("RisultatiTXT/" + nome_file + formato_testo, 'w', encoding='utf-8') as f:
        f.write(stampa)
    risultato = Diagnosticatore(lista_chiusure, lista_cammini_diagnosi, spazio_chiusure.nome_rete)
    conv_json.CreaJSONdaRete("RisultatiJSON/" + nome_file + formato_json, risultato)

    return Diagnosticatore(lista_chiusure, lista_cammini_diagnosi, spazio_chiusure.nome_rete)





def ricava_chiusura(nodo_iniziale,spazio_comportamentale,id,nodi_finali):
    #Inizializzo le variabili di utilità
    lista_cammini=copy.deepcopy(spazio_comportamentale.lista_cammini)
    lista_nodi_chiusura=[]
    coda_nodi=[]
    lista_cammini_chiusura=[]
    lista_nodi_uscenti=[]
    lista_nodi_chiusura.append(nodo_iniziale)
    coda_nodi.append(nodo_iniziale)
    cammini_esaminati = []
    #Finché la coda noda non è vuota
    while coda_nodi:
        for cammino in lista_cammini:
            if cammino.nodo_iniziale.id==coda_nodi[0].id:#per ogni cammino con nodo iniziale il nodo esaminato
                if cammino.oss=='\u03b5':
                    if cammino not in lista_cammini_chiusura:
                        lista_cammini_chiusura.append(cammino)#appendo il cammino con etichetta di osservabilità nulla
                    if not any(nodo for nodo in lista_nodi_chiusura if nodo.id==cammino.nodo_finale.id):
                        lista_nodi_chiusura.append(cammino.nodo_finale)# se non è già presente nella lista nodi appendo il nodo finale del cammino
                    if not any(nodo for nodo in coda_nodi if nodo.id==cammino.nodo_finale.id):
                        if not any(cammino_ex for cammino_ex in cammini_esaminati if cammino_ex==cammino):
                            coda_nodi.append(cammino.nodo_finale)# se non è già presente nella coda nodi e se il cammino non è ancora stato esaminato appendo il nodo finale del cammino
                            cammini_esaminati.append(cammino)
                else:
                    if not any(nodo for nodo in lista_nodi_uscenti if nodo.id == cammino.nodo_iniziale.id):
                        lista_nodi_uscenti.append(cammino.nodo_iniziale)#se il cammino ha etichetta di osservabilità diverso da nulla allora aggiungo il nodo iniziale a lista nodi uscenti, mi servirà per calcolare le decorazioni dei cammini dello spazio delle chiusure

        coda_nodi.remove(coda_nodi[0]) #rimuovo il nodo analizzato
    #Assegno ai nodi della chiusura l'attributo final
    final=False
    for nodo in lista_nodi_chiusura:
        for nodo2 in nodi_finali:
            if nodo.id==nodo2.id:
                final=True
    return ChiusuraSilenziosa(nodo_iniziale,lista_nodi_chiusura,lista_cammini_chiusura,id=id,lista_nodi_uscenti=lista_nodi_uscenti, final=final)

# def elimina_cammini_doppi_chiusura(chiusura):
#     x = 0
#     while x < len(chiusura.lista_cammini) - 1:
#         y = x + 1
#         while y < len(chiusura.lista_cammini):
#             if chiusura.lista_cammini[x] == chiusura.lista_cammini[y] and x != y:
#                 # print("test"+str(nodi_out[x].id)+str(nodi_out[y].id))
#                 chiusura.lista_cammini.remove(chiusura.lista_cammini[y])
#             else:
#                 y = y + 1
#         x = x + 1
#     return chiusura

def correzione_label_chiusura(label_chiusura):
    label_nuova=label_chiusura.split('|')

    #primo step se ho più di un elemento vedo se c'è la label epsilon e la rimuovo
    elimina_vuoto=False
    if len(label_nuova) > 1:
        for i in label_nuova:
            if "*" in i:
                elimina_vuoto=True
        if elimina_vuoto==True:
            for i in label_nuova:
                if i=='\u03b5':
                    label_nuova.remove(i)
    else:
        return label_nuova[0]
    #se c'era ora len è 1 e ritorno il rimanente, altrimenti passo a step sotto (ovviamente se c'erano 3 o + elementi il discorso cambia)
    if len(label_nuova) == 1:
        return label_nuova[0]
    else:
        if elimina_vuoto == True:
            x = 0
            while x < (len(label_nuova) - 1):
                y = x + 1
                while y < len(label_nuova):
                    if label_nuova[y] in label_nuova[x]:
                        label_nuova.remove(label_nuova[y])
                    else:
                        y = y + 1
                x = x + 1
            finale = ""
            for i in label_nuova:
                finale += i + "|"
            finale = finale[:-1]
            return finale
        else:
            return label_chiusura

