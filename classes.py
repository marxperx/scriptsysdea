# coding: utf-8

#############################################################################

# Classes do projeto

#############################################################################
from os import path
import csv
import random
import math


#############################################################################
#		Banco de candidatos
#############################################################################

#############################################################################

#		O perfil dos candidatos se configura no arquivo bancodecandidatos.conf 
#		É possível alterar a proporção dos níveis sorteados. 
#		
#############################################################################


class BancoDeCandidatos:																# Um banco contém uma lista de candidatos e uma lista de perfis
	def __init__(self):																	# Esta variável se configura com o arquivo específico
		self.listaCandidatos = []														# Declara a lista de candidatos (instâncias)
		self.listaPerfis =[]															# Um perfil significa um tipo de candidato, por exemplo, nível 3
		self.contagem = 0																# Um contador interno
		p = path.realpath('Inputs/bancodecandidatos.csv')								# Define a path para o arquivo de configuração		
		
		with open(p) as csv_file:														# Do arquivo de configuração são carregados os tipos e as respectivas qtds.
			next(csv_file)
			perfisDeCandidato = csv.reader(csv_file, delimiter = ';')
			for row in perfisDeCandidato:
				temp = PerfilDeCandidatos(int(row[0]), int(row[1]))
				self.listaPerfis.append(temp)

		for y in range(len(self.listaPerfis)):											# Com os tipos definidos, o banco de fato cria as instâncias individuais
			for x in range(int(self.listaPerfis[y].numero)):
				temp = Candidato(self.contagem,self.listaPerfis[y].nivel)
				self.listaCandidatos.append(temp)
				self.contagem += 1

		random.shuffle(self.listaCandidatos)											# Embaralha a lista. O id respeita a ordem inicial, mas o índice da lista não.

#############################################################################
#		Candidatos
#############################################################################

class Candidato:
	def __init__(self,idCandidato,nivel):
		self.idCandidato = idCandidato													# Identificação do candidato
		self.nivel = nivel																# O nível daquele candidato, que para fins de simulação, será o nível da prova
		self.listaDeQuestoesInterditadas = []											# Cada candidato tem uma lista de questões com que ele já entrou em contato

#############################################################################
#		Configuração
#############################################################################

class Configuracao:
	def __init__(self):																	# Rotina de início
		self.itens = []																	# Declara lista de itens
		p = path.realpath('Inputs/configuracoes.csv')									# Aponta para o arquivo de configurações, de onde serão extraídas as outras infos

		with open(p) as csv_file:														# Lê o arquivo de configurações
			next(csv_file)																# Pula a primeira linha, com os cabeçalhos
			itensDeConfiguracao = csv.reader(csv_file, delimiter =';')					# Lê os itens de configuração e os carrega como um csv reader
			for row in itensDeConfiguracao:												# Para cada linha nos itens de configuração
				temp = ItemDeConfiguracao(int(row[0]),row[1], row[2], row[3])			# Cria um item de configuração com os parâmetros contidos na linha
				self.itens.append(temp)													# Acrescenta o item à lista de itens de configuração

	def ImprimirItens(self):															# Imprime os itens de configuração (função para teste)
		for l in self.itens:
			id = l.id
			nome = l.nome
			tipo = l.tipo
			conteudo = l.conteudo

			print(f"Id={id},Nome={nome},Tipo={tipo},Conteudo={conteudo}")
	
	def EncontrarItem(self, valor):
		id = -1		
		for x in self.itens:
			if (x.id == valor) or (x.nome == valor) or (x.tipo == valor) or (x.conteudo == valor): 
				id = x.id
		return id			

#####################################################################################################################################################################
#####################################################################################################################################################################

class Instancia:																	# Na criação da instância da prova ocorre todo o sorteio das questões.
	def __init__(self, id, candidato, regime):										# A prova começa com os dados básicos: id da prova, candidato, regime da prova
		self.id = id
		self.candidato = candidato
		self.regime = regime

		
		slotsProva = SlotsLista()																			# Lista primária de slots da prova, retirada do arquivo
		self.planilhaDeControleDeSorteio = PlanilhaDeControleDeSorteio(candidato, regime, id, slotsProva)	# Inicia a planilha de controle do sorteio
		del slotsProva
		self.planilhaDePoolConjunto = PlanilhaDePoolConjunto(self.planilhaDeControleDeSorteio)					# Inicia as planilhas de pool
		self.planilhaTags = PlanilhaDeTags(self.planilhaDeControleDeSorteio)											# Inicia as planilhas de tag
		stacks = StacksLista()
		questaotagconjunto = QuestaoTagConjunto()
		self.planilhaStacks = PlanilhaDeStack(self)																# definir as variáveis necessárias para a planilha de stacks
		

#####################################################################################################################################################################
#####################################################################################################################################################################


class ItemDeConfiguracao:															# Um item de configuração é uma opção para configurar o script
	def __init__(self, id, nome, tipo, conteudo):									# Os parâmetros serão passados no momento de declarar o item
		self.id = id																# O primeiro parâmetro é o id do item
		self.nome = nome															# Ele terá um nome também
		self.tipo = tipo															# Um tipo
		self.conteudo = conteudo													# E um conteúdo, que pode ser, por exemplo, o endereço de um arquivo. 

class PerfilDeCandidatos:
	def __init__(self,nivel,numero):
		self.nivel = nivel
		self.numero = numero

class PlanilhaDeControleDaRodada:
	def __init__(self, idInstancia, idSlot, idModelo):								# Essa entidade representa o cabeçalho da tabela
		self.idInstancia = idInstancia												# int O número da instância de prova
		self.idSlot = idSlot														# int O id do slot a que essa tabela pertence
		self.idModelo = idModelo													# int O id do modelo sob o qual o sistema sorteia
		self.numeroSorteado = -1													# int O número de sorteio da 'loteria federal'
		self.questaoSorteada = -1													# int O id questão escolhida a partir do sorteio da 'loteria'
		self.occ = -1																# int Ocorrências
		qbb = 10000																	# int A quantidade básica de bilhetes a ser atribuída a cada questão no sorteio da rodada

		self.registros = []															# entidade Os registros dessa tabela, que serão em 'PlanilhasDeControleDaRodadaRegistro'.

class PlanilhaDeControleDaRodadaRegistro:											# Esses registros estão ligados à 'PlanilhaDeControleDaRodada', o cabeçalho
	def __init__(self, idQuestao,modificadorTags, qbb):
		self.idQuestao = idQuestao													# int O id da questão
		self.modificadorTags = modificadorTags										# float O valor combinado das tags aplicadas, que altera a Qbf
																			
		self.qbf = math.trunc(qbb * self.modificadorTags)							# int O valor de bilhetes efetivamente atribuído.
		self.lowRange = -1															# int O valor do menor bilhete no intervalo, inclusive
		self.highRange = -1															# int O valor do maior bilhete no intervalo, inclusive

#############################################################################
#		Planilha de controle do sorteio
#		Essa planilha efetivamente controla o sorteio da instância
#############################################################################

class PlanilhaDeControleDeSorteio:												
	def __init__(self, candidato, regime, instancia, slots):
		self.registro = []
		self.modelo = 0
		self.candidato = candidato.idCandidato
		self.instancia = instancia
		self.slots = slots															#Contém uma lista dos slots daquele modelo de prova, com informações correlatas
		p = path.realpath('Inputs/modelo.csv')
		p2 = path.realpath('Inputs/stacksslots.csv')
		csv_file_array = []
		csv_file_array2 =[]

		with open(p,'rt') as csv_file:
			for row in csv.reader(csv_file, delimiter =';'):
				csv_file_array.append(row)
		
		self.modelo = int(csv_file_array[1][1])
			
		for slot in self.slots.listaSlots:										# Para cada slot do arquivo da planilha, cria um registro de controle
			temp = PlanilhaDeControleDeSorteioRegistro(slot)					# 
			self.registro.append(temp)

		with open(p2, 'rt') as csv_file2:										# Acescenta as listas de stacks para cada slot
			next(csv_file2)
			for row in csv.reader(csv_file2, delimiter = ';'):
				csv_file_array2.append(row)

		for registro in self.registro:
			for linha in csv_file_array2:
				if(int(registro.slot.idSlot) == int(linha[1])):
					registro.stacks.append(int(linha[0]))


class PlanilhaDeControleDeSorteioRegistro:									# A planilha de controle de sorteio para cada registro se compõe do slot, mais de outras info de instância
	def __init__(self,slot):												# tais quais 
		self.slot = slot													# o slot primário em si, como armazenado no arquivo de configuração
		self.stacks = []													# a lista de stacks associados àquele slot
		self.ocorrencia = 0													
		self.listaDeRodada = 0
		self.conteudo = -1
		self.planilhaDeControleDaRodada = []								 



##########################################################################
# Planilha de pool
##########################################################################

# Cada planilha de pool controla a lista de tags das questões de um pool de um slot
# Para cada slot é criada uma planilha de pool (ainda que repetida), de modo a ter a mão a lista das tags, que será conferida a cada 
# Sorteio. Cada registro da planilha de pool terá o Id da questão e uma lista de Tags.

class PlanilhaDePool:															
	def __init__(self, id, slot, pool):
		self.id = id
		self.pool = pool
		self.slot = slot														#Contém o número do slot que a tabela controla
		self.registros = []														#Contém todos os registros da tabela, basicamente tags e listas de tags
		p =  path.realpath('Inputs/pool.csv')
		p2 = path.realpath('Inputs/questoestags.csv')
		csv_file_array_pool =[]													#Copia o arquivo pool.conf
		csv_file_array_tags = []												#Copia o arquivo tag.conf

		with open(p, 'rt') as csv_file:
			for row in csv.reader(csv_file, delimiter = ';'):
				csv_file_array_pool.append(row)
		with open(p2, 'rt') as csv_file2:
			for row in csv.reader(csv_file2, delimiter = ';'):
				csv_file_array_tags.append(row)

		for x in range(1,len(csv_file_array_pool)):
			numeroDoPool = int(csv_file_array_pool[x][1])
			if(numeroDoPool == pool):
				numeroDaQuestao = int(csv_file_array_pool[x][0])
				registro = PlanilhaDePoolRegistro(numeroDaQuestao)				#Cria um registro
				for x in range(1,len(csv_file_array_tags)):
					numeroDeQuestaoTag = int(csv_file_array_tags[x][0])
					if numeroDeQuestaoTag == numeroDaQuestao:
						temp = int(csv_file_array_tags[x][1])
						registro.listaTags.append(temp)
				self.registros.append(registro)

class PlanilhaDePoolConjunto:													# Implementa o conjunto de planilhas de pool para uma instância de prova
	def __init__(self, controleDeSorteio):
		self.PlanilhasDePool = []												# Esse é o conjunto de planilhas de pool a serem usadas na instância
		counting = 0
		for registro in controleDeSorteio.slots.listaSlots:
			temp = PlanilhaDePool(counting, registro.idSlot, registro.pool)
			self.PlanilhasDePool.append(temp)

class PlanilhaDePoolRegistro:
	def __init__(self, idQuestao):
		self.idQuestao = idQuestao
		self.listaTags = []

class PlanilhaDeStack:															# Nível de planilha, planilha descrita no documento
	def __init__(self, instancia):
		registros = []
		listaStacks = set()

		for line in instancia.planilhaDeControleDeSorteio.registro:
			for registro in line.stacks:
				listaStacks.add(registro)
		self.listaStacks = listaStacks

		p = path.realpath('Inputs/questoestags.csv')

																

class PlanilhaDeStackRegistros:
	def __init__(self, tag, ocorrencias, peso):
		self.tag = tag														# Integer, indicando qual a tag
		self.ocorrencias = ocorrencias
		self.peso = peso



##############################################################################################################
# Planilhas de tags
##############################################################################################################

# Para cada tag presente nas planilhas de pool, o sistema cria um registro de tags, listando também seu tipo e peso

class PlanilhaDeTags:
	def __init__(self,controleSorteio):
		self.listaTags = []
		self.listaTipoTags = []
		
		p = path.realpath('Inputs/tags.csv')
		p2 = path.realpath('Inputs/tipodetags.csv')
		csv_file_array_tipos = []
		csv_file_array_tags = []

		with open(p, 'rt') as csv_file:									#Importa as tags
			for row in csv.reader(csv_file, delimiter = ';'):
				csv_file_array_tags.append(row)

		with open(p2, 'rt') as csv_file:								#Importa os tipos de tags
			for row in csv.reader(csv_file, delimiter = ';'):
				csv_file_array_tipos.append(row)

		for x in range(1,len(csv_file_array_tipos)):
			temp = TipoDeTag(int(csv_file_array_tipos[x][0]),str(csv_file_array_tipos[x][1]))
			self.listaTipoTags.append(temp)

		for y in range(1,len(csv_file_array_tags)):
			temp = Tag(int(csv_file_array_tags[y][0]),int(csv_file_array_tags[y][1]), str(csv_file_array_tags[y][2]), int(csv_file_array_tags[y][3]))
			self.listaTags.append(temp)

##################################################################
#  Slots das versões
#  Cada slot contém um pool, uma parte, uma posição, uma descrição e um id. 
#  Não há stacks diretamente associados a slots aqui, porque no arquivo de configuração há uma tabela 
##################################################################
class QuestaoTagConjunto:
	def __init__(self):
		p =  path.realpath('Inputs/questoestags.csv')
		self.listaQuestoesTags = []

		with open(p,'rt') as csv_file:
			next(csv_file)																	# Pula a primeira linha do arquivo de configuração
			registroLine = csv.reader(csv_file, delimiter =';')									
			for row in registroLine:
				temp = QuestaoTag(int(row[0]),int(row[1]))
				self.listaQuestoesTags.append(temp)		

class QuestaoTag:
	def __init__(self, id, tag):
		self.id = id
		self.tag = tag

class Slot:
	def __init__(self, idSlot, parte, posicao, descricao, pool):
		self.idSlot = idSlot
		self.parte = parte
		self.posicao = posicao
		self.descricao = descricao
		self.pool = pool


##################################################################
#  Slots das versões de prova
#  Depois de importado do arquivo de configuração, cada slot se torna
#  Um item da lista de slots   
##################################################################

class SlotsLista:																		
	def __init__(self):
		self.listaSlots = []
		p =  path.realpath('Inputs/slots.csv')

		with open(p,'rt') as csv_file:
			next(csv_file)																	# Pula a primeira linha do arquivo de configuração
			slotLine = csv.reader(csv_file, delimiter =';')									
			for row in slotLine:
				temp = Slot(int(row[0]),int(row[1]),int(row[2]),str(row[3]), int(row[4]))
				self.listaSlots.append(temp)												

class Stack:
	def __init__(self, id, nome, tipo, regime, onset, cumulativo, magnitude):
		self.id = id																		# Integer designando chave primária
		self.nome = nome																	# Nome do stack
		self.tipo = tipo																	# Tipo de tag que aquele stack controla
		self.regime = regime																# Regime pode ser 'Gradual' ou 'Binário'
		self.onset = onset																	# Onset é um integer entre 0 e 3
		self.cumulativo = cumulativo														# Cumulativo é um integer, 0 ou 1
		self.magnitude = magnitude															# Magnitude é um decimal entre -1 e 9

class StacksLista:
	def __init__(self):
		self.listaStacks = []
		p = path.realpath('Inputs/stacks.csv')

		with open (p, 'rt') as csv_file:
			next(csv_file)
			slotLine = csv.reader(csv_file, delimiter = ';')
			for row in slotLine:
				temp = Stack(int(row[0]),str(row[1]), int(row[2]), str(row[3]), int(row[4]), int(row[5]), float(str(row[6]).replace(",",".")))
				self.listaStacks.append(temp)

class Tag:																					# Só a Tag3 está sendo importada
	def __init__(self, tipoTag, idTag, nome, pesoTag ):
		self.tipoTag = tipoTag
		self.idTag = idTag
		self.nome = nome
		self.pesoTag = pesoTag
		

class TipoDeTag:
	def __init__(self, id, nome):
		self.id = id
		self.nome = nome