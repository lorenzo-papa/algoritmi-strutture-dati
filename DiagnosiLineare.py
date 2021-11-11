import copy

import strutture_dati
from strutture_dati import *
import CreaReteJSON as conv_json
def diagnosiLineare(diagnosicatore, osservazione, stampare):
    stampa = ""

    for label in osservazione:
        label_esistente = False
        for cammino in diagnosicatore.lista_cammini:
            if cammino.oss == label:
                label_esistente = True
        if label_esistente == False:
            stampa += "L'etichetta " + label + " non è presente tra le possibili etichette di osservabilità"
            if stampare == 1:
                print(stampa)
            #risultato = {}
            return 0

    stringaOss = ""
    stringa_nome_file=""
    for label in osservazione:
        stringaOss += label + ", "
        stringa_nome_file+=label
    stringaOss = stringaOss[:-2]

    stampa += "Diagnosi di spazio comportamentale attraverso spazio delle chiusure relativo all'osservazione ["+ stringaOss+"]" +" e alla rete "+diagnosicatore.nome_rete + "\n\n"  # conterrà il risultato finale
    #Prendo i parametri da diagnosticatore
    lista_chiusure=copy.deepcopy(diagnosicatore.lista_chiusure)
    lista_cammini=copy.deepcopy(diagnosicatore.lista_cammini)

    #Creo stato iniziale con prima chiusura e etichetta nulla
    stato_iniziale=StatoDiagnosi(lista_chiusure[0],'\u03b5')
    coda_stati = []
    #appendo lo stato iniziale alla coda stati
    coda_stati.append(stato_iniziale)

    for label in osservazione:
        coda_stati_nuovo = []
        for stato_corrente in coda_stati:
            for cammino in lista_cammini:
                if cammino.oss==label and cammino.chiusura_iniziale.id==stato_corrente.chiusura.id:#
                    nuova_label = gestioneLabelNOAutotrans(stato_corrente.label,cammino.etichetta_diagnosi)
                    aggiungi=True
                    for stato in coda_stati_nuovo:
                        if stato.chiusura.id==cammino.chiusura_finale.id:
                            nuova_label = stato.label +"|"+ nuova_label
                            nuova_label = riscrittura_label(nuova_label)
                            nuovo_stato = StatoDiagnosi(cammino.chiusura_finale, nuova_label)
                            coda_stati_nuovo.append(nuovo_stato)
                            coda_stati_nuovo.remove(stato)
                            aggiungi=False
                            #break
                    if aggiungi==True:
                        nuovo_stato = StatoDiagnosi(cammino.chiusura_finale, nuova_label)
                        coda_stati_nuovo.append(nuovo_stato)

        coda_stati=coda_stati_nuovo

    for stato in coda_stati:
        if stato.chiusura.final==False:
            coda_stati.remove(stato)
    if len(coda_stati)==1:
        R="("+coda_stati[0].label+")"+"("+coda_stati[0].chiusura.diagnosi_relativa+") "
    elif len(coda_stati)==0:
        R="Errore, coda stati vuota, non son presenti stati di accettazione "
    else:
        R=""
        for stato in coda_stati:
            R+="("+stato.label+")"+"("+stato.chiusura.diagnosi_relativa+")"+"|"

    if len(coda_stati) == 1:
        R = "(" + coda_stati[0].label + ")" + "(" + coda_stati[0].chiusura.diagnosi_relativa + ") "
        etichetta = gestioneLabelNOAutotrans(coda_stati[0].label, coda_stati[0].chiusura.diagnosi_relativa)


    elif len(coda_stati) == 0:
        R = "Errore, coda stati vuota, non son presenti stati di accettazione "
        etichetta = "Errore, coda stati vuota, non son presenti stati di accettazione"
    else:
        R = ""
        etichetta = ""
        for stato in coda_stati:
            R += "(" + stato.label + ")" + "(" + stato.chiusura.diagnosi_relativa + ")" + "|"
            etichetta += gestioneLabelNOAutotrans(stato.label, stato.chiusura.diagnosi_relativa) + "|"
        etichetta = etichetta[:-1]
        etichetta = riscrittura_label(etichetta)

    R = R[:-1]
    stampa += "\nRisultato originale del metodo:\n" + R
    stampa += "\nRisultato elaborato del metodo:\n" + etichetta

    if stampare==1:
        print(stampa)

    formato_testo = ".txt"
    formato_json = ".json"
    nome_file = "DiagnosiChiusure-" + diagnosicatore.nome_rete + "-" + stringa_nome_file
    with open("RisultatiTXT/" + nome_file + formato_testo, 'w', encoding='utf-8') as f:
        f.write(stampa)

    conv_json.CreaJSONdaRete("RisultatiJSON/" + nome_file + formato_json, R)

    return R


def gestioneLabelNOAutotrans(cammino_in,cammino_out):
    lista_cammino_precedente = cammino_in.split("|")
    lista_cammino_seguente = cammino_out.split("|")
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
        finale += z + "|"  # nel caso str(z)
    finale = finale[:-1]
    return finale


def riscrittura_label(final):#camminoDoppio,listaCammini

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
