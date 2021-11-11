class FA:
    def __init__(self, stati, transizioni, stato_iniziale, stato_corrente,nome=""):
        self.nome = nome
        self.stati = stati
        self.transizioni = transizioni
        self.stato_iniziale = stato_iniziale
        self.stato_corrente = stato_corrente


class Stato:
    def __init__(self, nome=""):
        self.nome = nome


class Link:
	def __init__(self, FA_i=None, FA_f=None, nome="", buffer=''):
		self.nome = nome

		self.FA_i = FA_i
		self.FA_f = FA_f
		self.buffer = buffer

class Evento:
	def __init__(self, nome = ''):
		self.nome = nome


class FunzioneEvento:
	def __init__(self, evento=Evento(), link=Link()):
		self.link = link
		self.evento = evento

class Transizione:
	def __init__(self, stato_i, stato_f, nome="", evento_in = FunzioneEvento(), eventi_out = [], oss = '\u03b5', ril = '\u03b5'):
		self.nome = nome
		self.stato_i = stato_i
		self.stato_f = stato_f
		self.evento_in = evento_in
		self.eventi_out = eventi_out
		self.oss = oss
		self.ril = ril

class Rete:
	def __init__(self, lista_FA, lista_link,nome):
		self.lista_FA = lista_FA
		self.lista_link = lista_link
		self.nome=nome

class Nodo:
	def __init__(self, stati_FA, lista_link, id=0, final=False, indice_oss=0):
		self.stati_FA=stati_FA
		self.lista_link=lista_link
		self.nome=":".join(stati_FA) +"|" + ":".join(link.buffer for link in lista_link)
		self.id=id
		self.final=final
		self.indice_oss=indice_oss

class Cammino:
	def __init__(self, nodo_iniziale, nodo_finale, nome='', oss='\u03b5', ril='\u03b5', nodo_accettazione_raggiunto=None, etichetta_diagnosi='\u03b5', chiusura_iniziale=None, chiusura_finale=None):
		self.nome = nome

		self.nodo_iniziale = nodo_iniziale
		self.nodo_finale = nodo_finale
		self.oss = oss
		self.ril = ril
		self.chiusura_iniziale=chiusura_iniziale
		self.chiusura_finale=chiusura_finale
		self.nodo_accettazione_raggiunto = nodo_accettazione_raggiunto
		self.etichetta_diagnosi=etichetta_diagnosi

class SpazioComportamentale:
	def __init__(self, nodo_iniziale, lista_nodi, lista_cammini, nome_rete):
		self.nodo_iniziale=nodo_iniziale
		self.lista_nodi=lista_nodi
		self.lista_cammini=lista_cammini
		self.nome_rete=nome_rete


class SpazioComportamentaleOss:
	def __init__(self, nodo_iniziale, lista_nodi, lista_cammini,nome_rete, osservazione):
		self.nodo_iniziale=nodo_iniziale
		self.lista_nodi=lista_nodi
		self.lista_cammini=lista_cammini
		self.nome_rete=nome_rete
		self.osservazione=osservazione


class ChiusuraSilenziosa:
	def __init__(self,nodo_iniziale,lista_nodi,lista_cammini, id=0, diagnosi_relativa='\u03b5',lista_nodi_uscenti=[], final=False):
		self.nodo_iniziale=nodo_iniziale
		self.lista_nodi=lista_nodi
		self.lista_nodi_uscenti = lista_nodi_uscenti
		self.lista_cammini=lista_cammini
		self.id=id
		self.final = final
		self.diagnosi_relativa=diagnosi_relativa

class SpazioChiusure:
	def __init__(self,lista_chiusure, lista_cammini,nodi_finali, nome_rete):
		self.lista_chiusure=lista_chiusure
		self.lista_cammini=lista_cammini
		self.nodi_finali=nodi_finali
		self.nome_rete=nome_rete

class Diagnosticatore:
	def __init__(self,lista_chiusure, lista_cammini, nome_rete):
		self.lista_chiusure=lista_chiusure
		self.lista_cammini=lista_cammini
		self.nome_rete=nome_rete


class StatoDiagnosi:
	def __init__(self,chiusura,label):
		self.chiusura=chiusura
		self.label=label