import pickle
from strutture_dati import *

state0s = Stato(nome = '0')
state1s = Stato(nome = '1')

state0b = Stato(nome = '0')
state1b = Stato(nome = '1')

s1 = Transizione(state0s, state1s, oss = 'act', nome = 's1')
s2 = Transizione(state1s, state0s, oss = 'sby', nome = 's2')
s3 = Transizione(state0s, state0s, ril = 'f1', nome = 's3')
s4 = Transizione(state1s, state1s, ril = 'f2', nome = 's4')

b1 = Transizione(state0b, state1b, oss = 'opn', nome = 'b1')
b2 = Transizione(state1b, state0b, oss = 'cls', nome = 'b2')
b3 = Transizione(state0b, state0b, ril = 'f3', nome = 'b3')
b4 = Transizione(state1b, state1b, ril = 'f4', nome = 'b4')
b5 = Transizione(state0b, state0b, oss = 'nop', nome = 'b5')
b6 = Transizione(state1b, state1b, oss = 'nop', nome = 'b6')
b7 = Transizione(state0b, state1b, ril = 'f5', oss = 'opn', nome = 'b7')
b8 = Transizione(state1b, state0b, ril = 'f6', oss = 'cls', nome = 'b8')



list_state_S = [state0s, state1s]
list_transition_S = [s1, s2, s3, s4]

S = FA(list_state_S, list_transition_S, stato_iniziale = state0s, stato_corrente = state0s, nome = 'S')

list_state_B = [state0b, state1b]
list_transition_B = [b1, b2, b3, b4, b5, b6, b7, b8]

B = FA(list_state_B, list_transition_B, stato_iniziale = state0b, stato_corrente = state0b, nome = 'B')


L = Link(S.nome, B.nome, nome = 'L')

op = Evento(nome = 'op')
cl = Evento(nome = 'cl')

function_opL = FunzioneEvento(op, L)
function_clL = FunzioneEvento(cl, L)

s1.eventi_out = [function_opL]
s2.eventi_out = [function_clL]
s3.eventi_out = [function_clL]
s4.eventi_out = [function_opL]

b1.evento_in = function_opL
b2.evento_in = function_clL
b3.evento_in = function_opL
b4.evento_in = function_clL
b5.evento_in = function_clL
b6.evento_in = function_opL
b7.evento_in = function_clL
b8.evento_in = function_opL



rete3 = Rete([S, B], [L], "Rete 3")


