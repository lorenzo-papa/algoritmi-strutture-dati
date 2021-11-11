from strutture_dati import *


stato10 = Stato(nome = '10')
stato11 = Stato(nome = '11')

stato20 = Stato(nome = '20')
stato21 = Stato(nome = '21')

stato30 = Stato(nome = '30')
stato31 = Stato(nome = '31')

t1a = Transizione(stato10, stato11, nome = 't1a')
t1b = Transizione(stato11, stato10, nome = 't1b')
t1c = Transizione(stato10, stato11, nome = 't1c', ril = 'f1')

t2a = Transizione(stato20, stato21, nome = 't2a', oss = 'o1')
t2b = Transizione(stato21, stato20, nome = 't2b', oss = 'o2')

t3a = Transizione(stato30, stato31, nome = 't3a')
t3b = Transizione(stato31, stato30, nome = 't3b')
t3c = Transizione(stato31, stato31, nome = 't3c', ril = 'f3')

lista_stati_C1 = [stato10, stato11]
lista_transizioni_C1 = [t1a, t1b, t1c]

C1 = FA(lista_stati_C1, lista_transizioni_C1, stato_iniziale = stato10, stato_corrente = stato10, nome = 'C1')

lista_stati_C2 = [stato20, stato21]
lista_transizioni_C2 = [t2a, t2b]

C2 = FA(lista_stati_C2, lista_transizioni_C2, stato_iniziale = stato20, stato_corrente = stato20, nome = 'C2')

lista_stati_C3 = [stato30, stato31]
lista_transizioni_C3 = [t3a, t3b, t3c]

C3 = FA(lista_stati_C3, lista_transizioni_C3, stato_iniziale = stato30, stato_corrente = stato30, nome = 'C3')

L1 = Link(C2.nome, C1.nome, nome = 'L1')
L2 = Link(C2.nome, C3.nome, nome = 'L2')
L3 = Link(C3.nome, C1.nome, nome = 'L3')

e1 = Evento(nome = 'e1')
e2 = Evento(nome = 'e2')
e3 = Evento(nome = 'e3')

funzione_e1L1 = FunzioneEvento(e1, L1)
funzione_e2L3 = FunzioneEvento(e2, L3)
funzione_e3L2 = FunzioneEvento(e3, L2)

t1a.evento_in = funzione_e1L1
t1b.evento_in = funzione_e2L3

t2a.eventi_out = [funzione_e1L1,funzione_e3L2]

t2b.eventi_out = [funzione_e1L1]

t3a.eventi_out = [funzione_e2L3]

t3b.evento_in = funzione_e3L2

t3c.evento_in = funzione_e3L2

rete2 = Rete([C1, C2, C3], [L1, L2, L3],"Rete 2")

