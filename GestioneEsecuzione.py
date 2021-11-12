import strutture_dati
import sys
import jsonpickle
import pickle
from tkinter import Tk, simpledialog
from tkinter.filedialog import askopenfilename
import re
import time
import tracemalloc
#gestione tipologia file, eccezioni e input vari

#metodo utile per richiedere il file in input all'utente (controlla sia json e convertibile nell'oggetto richiesto dalla funzionalità scelta)
def richiesta_file_conv():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected fileprint(filename)
    while filename is None or "":
        filename = askopenfilename()
    while checkFilename(filename) is False:
        filename = askopenfilename()
    f = open(filename)
    json_str = f.read()
    try:
        obj = jsonpickle.decode(json_str)
    except:
        print("Errore in conversione riprovare\n")

    return obj

#controllo formato json
def checkFilename(filename):
    if filename.endswith(('.json','.JSON')):
        return True
    else:
        print("Il formato del file in input è scorretto, si prega di fornire un file in formato .json\n")
        return False

#controllo l'input sia del tipo struttura dati Rete
def check_rete(rete):
    if not (isinstance(rete, strutture_dati.Rete)):
        #print("Il file inserito non rappresenta una Rete di automi a stati finiti,"
        #     " si prega di inserire un nuovo input corretto")
        return False
    else:
        return True

#controllo l'input sia del tipo struttura dati SpazioComportamentale
def check_spazio_comp(spazio_comp):
    if not (isinstance(spazio_comp, strutture_dati.SpazioComportamentale)):
        #print("Il file inserito non rappresenta una Rete di automi a stati finiti,"
        #      " si prega di inserire un nuovo input corretto")
        return False
    else:
        return True

#controllo l'input sia del tipo struttura dati SpazioComportamentale relativo ad un'osservazione lienare
def check_spazio_oss(spazio_oss):
    if not (isinstance(spazio_oss, strutture_dati.SpazioComportamentaleOss)):
        #print("Il file inserito non rappresenta uno spazio comportamentale relativo ad un'osservazione lineare,"
        # "si prega di inserire un nuovo input corretto")
        return False
    else:
        return True

#controllo l'input sia del tipo struttura dati SpazioDelleChiusure
def check_spazio_chiusure(spazio_chiusure):
    if not (isinstance(spazio_chiusure,strutture_dati.SpazioChiusure)):
        #print("Il file inserito non rappresenta uno spazio delle chiusure,"
        #      "si prega di inserire un nuovo input corretto")
        return False
    else:
        return True

#controllo l'input sia del tipo struttura dati Diagnosticatore
def check_diagnosticatore(diagnosicatore):
    if not (isinstance(diagnosicatore,strutture_dati.Diagnosticatore)):
        # print("Il file inserito non rappresenta un diagnosticatore,"
        #     "si prega di inserire un nuovo input corretto")
        return False
    else:
        return True

#controllo che l'osservazione non sia vuota/nulla - richiamo check contenuto
def check_spazio_oss_label(oss):
    while oss is None or oss == "" or not oss or not oss.strip():  # or not test_root_password(root_password)
        return False
    while checkOss(oss) is False:
        return False
    return True

#controllo l'osservazione non sia un numero, elimino spazi
def checkOss(oss):
    try:
        # Convert it into integer
        val = int(oss)
        print("L'input inserito è un integer. Numero = ", val)
        print("Si prega di inserire una stringa (ex. o1 oppure o1,o2)\n")
        return False
    except ValueError:
        try:
            # Convert it into float
            val = float(oss)
            print("L'input inserito è un float. Numero = ", val)
            print("Si prega di inserire una stringa (ex. o1 oppure o1,o2)\n")
            return False
        except ValueError:
            if " " in oss:
                oss=oss.replace(" ",",")
            if ',' in oss or '-' in oss or '#' in oss or '|' in oss or '.' in oss:
                try:
                    check = re.split('[-+#|,.]', oss)
                    for i in check:
                        val=int(i)
                    print("L'input inserito è una lista di numeri integer o float")
                    print("Si prega di inserire una stringa (ex. o1 oppure o1,o2)\n")
                    return False
                except ValueError:
                    print("L'osservazione richiesta è stata accettata - Osservazione: ", str(oss))
                    print("L'input è corretto, si procede al calcolo richiesto\n")
                    return True
            else:
                print("L'osservazione richiesta è stata accettata - Osservazione: ", str(oss))
                print("L'input è corretto, si procede al calcolo richiesto\n")
                return True

#controllo il tipo di oggeto in input al programma
def check_obj_type(obj):
    if (isinstance(obj, strutture_dati.Rete)):
        return 1
    elif (isinstance(obj, strutture_dati.SpazioComportamentale)):
        return 2
    elif (isinstance(obj, strutture_dati.SpazioComportamentaleOss)):
        return 3
    elif(isinstance(obj, strutture_dati.SpazioChiusure)):
        return 4
    elif(isinstance(obj, strutture_dati.Diagnosticatore)):
        return 5
    else:
        print("File non riconosciuto\n")

#continuo a chiedere la label finchè l'input non è corretto
def richiesta_label(oss):
    while check_spazio_oss_label(oss) is False:
        oss = simpledialog.askstring("Inserimento osservazione lineare",
                                     "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")
    # oss = oss.split(",|-|")
    oss=oss.strip()
    if " " in oss:
        oss = oss.replace(" ", ",")
    oss = re.split('[-+#|,.]', oss)
    return oss

#chiedo all'utente se vuole proseguire e controllo l'input
def proseguire(response):
    if response is None or response == "" or not response or not response.strip():
        return False
    try:
        # Convert it into integer
        val = int(response)
        print("L'input inserito è un integer. Numero = ", val)
        print("Si prega di inserire una risposta valida (s si yes y oppure n no")
        return False
    except ValueError:
        try:
            # Convert it into float
            val = float(response)
            print("L'input inserito è un float. Numero = ", val)
            print("Si prega di inserire una risposta valida (s si yes y oppure n no")
            return False
        except ValueError:
            response = response.lower().strip()
            if response=="s" or response=="si" or response=="y" or response=="yes":
                return 2
            elif response=="n" or response=="no":
                return 1
            else:
                print("Si prega di inserire una risposta valida (s si yes y oppure n no")
                return False

#metodi per la raccolta dei dati di performance
def raccolta_performance_start():
    start_time = time.process_time()
    tracemalloc.start()
    return (start_time)

def raccolta_performance_end(start_time):
    end_time = time.process_time()
    tot_time = end_time - start_time
    final_space=tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("Tempo impiegato per l'esecuzione (s): ",str(tot_time))
    print("Totale memoria allocata (Byte): ", str(final_space[0]),"dimensione corrente tracciata\t",str(final_space[1]),"picco durante l'esecuzione\n")
    return (tot_time,final_space)

