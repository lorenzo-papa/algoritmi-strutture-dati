import json
import timeit
import tracemalloc
from tkinter.filedialog import askopenfilename

import Spazio_Comportamentale as sc
import rete2
import Osservazione_Lineare as ol
import EspressioneRegolare2 as er2
from tkinter import Tk, simpledialog
import DiagnosiOsservazione as do
import EspressioniRegolari as eri
import Diagnosticatore as di
import time
import rete1
import rete2
import rete3
import CasoStudio
import DiagnosiLineare as dl
import jsonpickle
import pickle
import CreaReteJSON as creaRete
import numpy as np
import GestioneEsecuzione as ge
import sys
import re

#invocazione main
if __name__ == "__main__":

    print("Benvenuto. Il programma permette di realizzare le seguenti funzioni:")
    print("1)Generazione dello spazio comportamentale\n"
          "2)Generazione dello spazio comportamentale relativo ad una particolare osservazione lineare\n"
          "3)Calcolo della diagnosi relativa a una osservazione lineare\n"
          "4)Generazione dello spazio delle chiusure silenziose\n"
          "5)Generazione del diagnosticatore\n"
          "6)Calcolo della diagnosi lineare relativa a una osservazione lineare (basata su diagnosticatore)\n"
          "Da dove preferisci cominciare?")
    while True:
        oss=""
        x=input("Inserisci il numero corrispondente alla funzionalità, oppure 0 per uscire.\t")
        try:
            x=int(x)
            if x >= 0 and x < 7:
                if x==0:
                    break
                # input rete
                if x == 1:
                    print("\nHai scelto la funzione: Generazione dello spazio comportamentale")
                    print("Inserire in input il file relativo alla Rete (formato .json)")
                    obj = ge.richiesta_file_conv()
                    while ge.check_rete(obj) is False:
                        print("Il file inserito non rappresenta una Rete di automi a stati finiti,"
                             " si prega di inserire un nuovo input corretto")
                        obj = ge.richiesta_file_conv()
                    print("Caricamento del file eseguito correttamente")
                    initial_time=ge.raccolta_performance_start()
                    sc.spazio_comportamentale(obj, 1)
                    ge.raccolta_performance_end(initial_time)
                elif x == 2:
                    #input rete
                    print("\nHai scelto la funzione: Generazione dello spazio comportamentale relativo ad una particolare osservazione lineare")
                    print("Inserire in input il file relativo alla Rete (formato .json)")
                    obj = ge.richiesta_file_conv()
                    #prima controllo correttezza del file in input
                    while ge.check_rete(obj) is False:
                        print("Il file inserito non rappresenta una Rete di automi a stati finiti,"
                             " si prega di inserire un nuovo input corretto")
                        obj = ge.richiesta_file_conv()
                    print("Caricamento del file eseguito correttamente")
                    oss = simpledialog.askstring("Inserimento osservazione lineare",
                                                 "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")
                    #in seguito controllo la label in input
                    oss=ge.richiesta_label(oss)
                    initial_time = ge.raccolta_performance_start()
                    ol.osservazione_lineare(obj, oss, 1)
                    ge.raccolta_performance_end(initial_time)

                elif x == 3:
                    # rete - oppure spazio oss
                    print("\nHai scelto la funzione: Calcolo della diagnosi relativa a una osservazione lineare")
                    print("Puoi inserire in input o il file relativo alla Rete o il file relativo allo Spazio Comportamentale relativo ad un'Osservazione Lineare (formato .json)")
                    obj = ge.richiesta_file_conv()
                    while ge.check_rete(obj) is False and ge.check_spazio_oss(obj) is False:
                        print("Il file inserito non rappresenta nè una Rete di automi a stati finiti nè uno Spazio Comportamentale,"
                             " si prega di inserire un nuovo input corretto")
                        obj = ge.richiesta_file_conv()
                    print("Caricamento del file eseguito correttamente")
                    if ge.check_obj_type(obj)==1:
                        oss = simpledialog.askstring("Inserimento osservazione lineare",
                                                     "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")

                        oss=ge.richiesta_label(oss)
                        initial_time = ge.raccolta_performance_start()
                        spazio_oss=ol.osservazione_lineare(obj, oss, 1)
                        ge.raccolta_performance_end(initial_time)
                        if spazio_oss == 0:
                            print("Errore osservazione non presente nella rete, si prega di rieseguire il programma in maniera corretta")
                            sys.exit()
                        response = None
                        response=input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while(ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response)==2:
                            initial_time = ge.raccolta_performance_start()
                            do.diagnosiOsservazione(spazio_oss, 1)
                            ge.raccolta_performance_end(initial_time)
                    elif ge.check_obj_type(obj)==3:
                        initial_time = ge.raccolta_performance_start()
                        do.diagnosiOsservazione(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                elif x == 4:
                    #rete - spazio comp
                    print("\nHai scelto la funzione: Generazione dello spazio delle chiusure silenziose")
                    print("Puoi inserire in input il file relativo alla Rete o il file relativo allo Spazio Comportamentale (formato .json)")
                    obj = ge.richiesta_file_conv()
                    while ge.check_rete(obj) is False \
                            and ge.check_spazio_comp(obj) is False:
                        print("Il file inserito non rappresenta nè una Rete di automi a stati finiti nè uno Spazio Comportamentale,"
                            " si prega di inserire un nuovo input corretto")
                        obj = ge.richiesta_file_conv()
                    print("Caricamento del file eseguito correttamente")
                    if ge.check_obj_type(obj) == 1:
                        initial_time = ge.raccolta_performance_start()
                        spazio_comp=sc.spazio_comportamentale(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                        response = None
                        response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while (ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response) == 2:
                            initial_time = ge.raccolta_performance_start()
                            di.spazio_chiusure(spazio_comp, 1)
                            ge.raccolta_performance_end(initial_time)
                    elif ge.check_obj_type(obj) == 2:
                        initial_time = ge.raccolta_performance_start()
                        di.spazio_chiusure(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                    else:
                        print("Errore file in input")

                elif x == 5:
                    # rete - spazio comp - spazio chiusure
                    print("\nHai scelto la funzione: Generazione del diagnosticatore")
                    print("Puoi inserire in input il file relativo alla Rete o il file relativo allo Spazio Comportamentale o allo Spazio delle Chiusure (formato .json)")
                    obj = ge.richiesta_file_conv()
                    while ge.check_rete(obj) is False and ge.check_spazio_comp(obj) is False\
                            and ge.check_spazio_chiusure(obj) is False:
                        print(
                            "Il file inserito non rappresenta nè una Rete di automi a stati finiti nè uno Spazio Comportamentale nè uno Spazio delle Chiusure,"
                            " si prega di inserire un nuovo input corretto")
                        obj = ge.richiesta_file_conv()
                    print("Caricamento del file eseguito correttamente")
                    if ge.check_obj_type(obj) == 1:
                        initial_time = ge.raccolta_performance_start()
                        spazio_comp = sc.spazio_comportamentale(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                        response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while (ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response) == 2:
                            initial_time = ge.raccolta_performance_start()
                            spazio_chiusure = di.spazio_chiusure(spazio_comp, 1)
                            ge.raccolta_performance_end(initial_time)
                            response=None
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                            while (ge.proseguire(response)) is False:
                                response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                            if ge.proseguire(response) == 2:
                                initial_time = ge.raccolta_performance_start()
                                di.diagnosticatore(spazio_chiusure, 1)
                                ge.raccolta_performance_end(initial_time)
                    elif ge.check_obj_type(obj) == 2:
                        initial_time = ge.raccolta_performance_start()
                        spazio_chiusure=di.spazio_chiusure(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                        response = None
                        response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while (ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response) == 2:
                            initial_time = ge.raccolta_performance_start()
                            di.diagnosticatore(spazio_chiusure, 1)
                            ge.raccolta_performance_end(initial_time)
                    elif ge.check_obj_type(obj) == 4:
                        initial_time = ge.raccolta_performance_start()
                        di.diagnosticatore(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                    else:
                        print("Errore file in input")

                elif x == 6:
                    # rete - spazio comp - spazio chiusure - diagnosticatore
                    print("\nHai scelto la funzione: Calcolo della diagnosi lineare relativa a una osservazione lineare")
                    print("Puoi inserire in input il file relativo alla Rete o il file relativo allo Spazio Comportamentale o allo Spazio delle Chiusure o al Diagnosticatore (formato .json)")

                    obj = ge.richiesta_file_conv()
                    while ge.check_rete(obj) is False and ge.check_spazio_comp(obj) is False\
                            and ge.check_spazio_chiusure(obj) is False \
                            and ge.check_diagnosticatore(obj) is False:
                        print(
                            "Il file inserito non rappresenta nè una Rete di automi a stati finiti nè uno Spazio Comportamentale "
                            "nè uno Spazio delle Chiusure nè un Diagnosticatore,"
                            " si prega di inserire un nuovo input corretto")
                        obj = ge.richiesta_file_conv()
                    print("Caricamento del file eseguito correttamente")
                    #input rete
                    if ge.check_obj_type(obj) == 1:
                        initial_time = ge.raccolta_performance_start()
                        spazio_comp = sc.spazio_comportamentale(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                        response = None
                        response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while (ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response) == 2:
                            initial_time = ge.raccolta_performance_start()
                            spazio_chiusure = di.spazio_chiusure(spazio_comp, 1)
                            ge.raccolta_performance_end(initial_time)
                            response = None
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                            while (ge.proseguire(response)) is False:
                                response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                            if ge.proseguire(response) == 2:
                                initial_time = ge.raccolta_performance_start()
                                diagnosticatore=di.diagnosticatore(spazio_chiusure, 1)
                                ge.raccolta_performance_end(initial_time)
                                response = None
                                response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                                while (ge.proseguire(response)) is False:
                                    response = input(
                                        "Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                                if ge.proseguire(response) == 2:
                                    oss = simpledialog.askstring("Inserimento osservazione lineare",
                                                                 "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")
                                    oss = ge.richiesta_label(oss)
                                    initial_time = ge.raccolta_performance_start()
                                    dl.diagnosiLineare(diagnosticatore, oss, 1)
                                    ge.raccolta_performance_end(initial_time)
                    #input spazio comp
                    elif ge.check_obj_type(obj) == 2:
                        initial_time = ge.raccolta_performance_start()
                        spazio_chiusure = di.spazio_chiusure(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                        response = None
                        response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while (ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response) == 2:
                            initial_time = ge.raccolta_performance_start()
                            diagnosticatore = di.diagnosticatore(spazio_chiusure, 1)
                            ge.raccolta_performance_end(initial_time)
                            response = None
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                            while (ge.proseguire(response)) is False:
                                response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                            if ge.proseguire(response) == 2:
                                oss = simpledialog.askstring("Inserimento osservazione lineare",
                                                             "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")
                                oss = ge.richiesta_label(oss)
                                initial_time = ge.raccolta_performance_start()
                                dl.diagnosiLineare(diagnosticatore, oss, 1)
                                ge.raccolta_performance_end(initial_time)
                    # input spazio chiusure
                    elif ge.check_obj_type(obj) == 4:
                        initial_time = ge.raccolta_performance_start()
                        diagnosticatore = di.diagnosticatore(obj, 1)
                        ge.raccolta_performance_end(initial_time)
                        oss = simpledialog.askstring("Inserimento osservazione lineare",
                                                     "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")
                        oss = ge.richiesta_label(oss)
                        response = None
                        response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        while (ge.proseguire(response)) is False:
                            response = input("Vuoi proseguire? (valori accettati: si/no s/n y/n yes/not)")
                        if ge.proseguire(response) == 2:
                            initial_time = ge.raccolta_performance_start()
                            dl.diagnosiLineare(diagnosticatore, oss, 1)
                            ge.raccolta_performance_end(initial_time)
                    # input diagnoticatore
                    elif ge.check_obj_type(obj)==5:
                        oss = simpledialog.askstring("Inserimento osservazione lineare",
                                                     "Inserisci l'osservazione lineare (ex o1); se più di una usare il separatore (separatori accettati o1,o2 o1-o2 o1+o2 o1#o2 o1|o2):")
                        oss = ge.richiesta_label(oss)
                        initial_time = ge.raccolta_performance_start()
                        dl.diagnosiLineare(obj, oss, 1)
                        ge.raccolta_performance_end(initial_time)
                    else:
                        print("Errore file in input")

        except ValueError:
            print("Puoi inserire solo numeri da 1 a 6")


    print("Grazie e arrivederci.")

