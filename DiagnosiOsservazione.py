import strutture_dati
from strutture_dati import *
import EspressioneRegolare2 as es
import CreaReteJSON as conv_json
def diagnosiOsservazione(spazioOsservazione,stampare=0):
    stampa=""

    stampa += "Diagnosi di spazio comportamentale relativo all'osservazione ["+ spazioOsservazione.osservazione+"]" +" e alla rete "+spazioOsservazione.nome_rete + "\n\n"  # conterrà il risultato finale

    formato_testo = ".txt"
    formato_json = ".json"

    nome_file = "DiagnosiOL-" + spazioOsservazione.nome_rete + "-" + spazioOsservazione.osservazione
    risultato = es.EspressioneRegolare(spazioOsservazione, 0)
    stampa += risultato

    if stampare == 1:
        print(stampa)

    with open("RisultatiTXT/" + nome_file + formato_testo, 'w', encoding='utf-8') as f:
        f.write(stampa)
    conv_json.CreaJSONdaRete("RisultatiJSON/" + nome_file + formato_json, risultato)

    return risultato
