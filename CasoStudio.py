from strutture_dati import *

statoA1 = Stato(nome = 'S')
statoA2 = Stato(nome = 'I')#todo cambiare pulita e cera
statoA3 = Stato(nome = 'R')
#statoA4 = Stato(nome = 'C')

statoL0 = Stato(nome = '0')
statoL1 = Stato(nome = '1')
statoL2 = Stato(nome = '2')
#statoL3 = Stato(nome = '3')


tA1 = Transizione(statoA1, statoA2, nome = 'tASI')
tA2 = Transizione(statoA2, statoA3, nome = 'tAIR')
#tA3 = Transizione(statoA3, statoA4, nome = 'tARC', oss = 'c')


tL01 = Transizione(statoL0, statoL1, nome = 'tL01',oss="g1")
tL12 = Transizione(statoL1, statoL2, nome = 'tL12',oss="g2")
#tL23 = Transizione(statoL2, statoL3, nome = 'tL23')
tL21 = Transizione(statoL2, statoL1, nome = 'tL21',ril="o1")
#tL32 = Transizione(statoL3, statoL2, nome = 'tL32')
tL10 = Transizione(statoL1, statoL0, nome = 'tL10',ril="o2")
tL10r = Transizione(statoL1, statoL0, nome = 'tL10r',ril="r1")#todo prova con r1 r2
tL20 = Transizione(statoL2, statoL0, nome = 'tL20', ril="r2")
#tL30 = Transizione(statoL3, statoL0, nome = 'tL30')

# lista_stati_A = [statoA1, statoA2, statoA3,statoA4]
# lista_transizioni_A = [tA1, tA2,tA3]

lista_stati_A = [statoA1, statoA2, statoA3]
lista_transizioni_A = [tA1, tA2]

AA = FA(lista_stati_A, lista_transizioni_A, stato_iniziale = statoA1, stato_corrente = statoA1, nome = 'AA')


# lista_stati_L = [statoL0, statoL1, statoL2,statoL3]
# lista_transizioni_L = [tL01, tL12,tL23,tL10,tL20,tL30,tL21,tL32]

lista_stati_L = [statoL0, statoL1, statoL2]
lista_transizioni_L = [tL01, tL12,tL10,tL10r,tL20,tL21]


AL = FA(lista_stati_L, lista_transizioni_L, stato_iniziale = statoL0, stato_corrente = statoL0, nome = 'AL')

LAL = Link(AA.nome, AL.nome, nome = 'LAL')
LLA = Link(AL.nome, AA.nome, nome = 'LLA')

a = Evento(nome = 'azione')
s = Evento(nome = 'sottraigettone')

funzione_evento_LLA_a = FunzioneEvento(a, LLA) #TODO verifica se corretto
funzione_evento_LAL_s = FunzioneEvento(s, LAL)

tA1.evento_in=funzione_evento_LLA_a#deve avere gettone per iniziare
tA1.eventi_out=[funzione_evento_LAL_s]#deve sottrarre il soldo dopo aver agito

tA2.evento_in=funzione_evento_LLA_a#deve avere gettone per iniziare
tA2.eventi_out=[funzione_evento_LAL_s]#deve sottrarre il soldo dopo aver agito

# tA3.evento_in=funzione_evento_LLA_a#deve avere gettone per iniziare
# tA3.eventi_out=[funzione_evento_LAL_s]#deve sottrarre il soldo dopo aver agito

tL01.eventi_out=[funzione_evento_LLA_a]#do il potere di agire

tL12.evento_in=funzione_evento_LLA_a
tL12.eventi_out=[funzione_evento_LLA_a]#do il potere di agire

# tL23.evento_in=funzione_evento_LLA_a
# tL23.eventi_out=[funzione_evento_LLA_a]#do il potere di agire

tL10r.evento_in=funzione_evento_LLA_a#gli toglie la possibilità di agire

tL20.evento_in=funzione_evento_LLA_a#gli toglie la possibilità di agire

# tL30.evento_in=funzione_evento_LLA_a#gli toglie la possibilità di agire

tL10.evento_in=funzione_evento_LAL_s#gli toglie la possibilità di agire

tL21.evento_in=funzione_evento_LAL_s #vede se ha appena agito
tL21.eventi_out=[funzione_evento_LLA_a]

# tL32.evento_in=funzione_evento_LAL_s
# tL32.eventi_out=[funzione_evento_LLA_a]


rete = Rete([AA, AL], [LAL, LLA], "Caso di studio - Autolavaggio")




