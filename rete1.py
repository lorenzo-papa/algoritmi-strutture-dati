import pickle

from strutture_dati import *

stato20 = Stato(nome = '20')
stato21 = Stato(nome = '21')

stato30 = Stato(nome = '30')
stato31 = Stato(nome = '31')

t2a = Transizione(stato20, stato21, nome = 't2a', oss = 'o2')
t2b = Transizione(stato21, stato20, nome = 't2b', ril = 'r')

t3a = Transizione(stato30, stato31, nome = 't3a', oss = 'o3')
t3b = Transizione(stato31, stato30, nome = 't3b')
t3c = Transizione(stato31, stato31, nome = 't3c', ril = 'f')


lista_stati_C2 = [stato20, stato21]
lista_transizioni_C2 = [t2a, t2b]

C2 = FA(lista_stati_C2, lista_transizioni_C2, stato_iniziale = stato20, stato_corrente = stato20, nome = 'C2')

lista_stati_C3 = [stato30, stato31]
lista_transizioni_C3 = [t3a, t3b, t3c]

C3 = FA(lista_stati_C3, lista_transizioni_C3, stato_iniziale = stato30, stato_corrente = stato30, nome = 'C3')


L2 = Link(C3.nome, C2.nome, nome = 'L2')
L3 = Link(C2.nome, C3.nome, nome = 'L3')

e2 = Evento(nome = 'e2')
e3 = Evento(nome = 'e3')

funzione_evento_e2L2 = FunzioneEvento(e2, L2)
funzione_evento_e3L3 = FunzioneEvento(e3, L3)

t2a.evento_in = funzione_evento_e2L2
t2a.eventi_out = [funzione_evento_e3L3]

t2b.eventi_out = [funzione_evento_e3L3]

t3a.eventi_out = [funzione_evento_e2L2]


t3b.evento_in = funzione_evento_e3L3

t3c.evento_in = funzione_evento_e3L3

rete1 = Rete([C2, C3], [L2, L3], "Rete1") #lista FA e lista link

