# coding: utf-8

#############################################################################

#							Arquivo principal

#############################################################################

import classes as c
from os import path
import mensagens as m


#############################################################################

#						Procedimentos de inicialização

#############################################################################

configuracoes = c.Configuracao()											# Carrega informações de configuração do script. E.g., paths de arquivos I/O
banco = c.BancoDeCandidatos()												# Carrega um bancos de dados de candidatos, conforme configuração
mensagens = m.Dic()															# Carrega as mensagens-padrão do script


# O objetivo deste documento é gerar x instâncias. Por enquanto ele está gerando apenas uma instância. 

regime = 'Teste'


idProva = 1

inst = c.Instancia(idProva,banco.listaCandidatos[0],regime)					# Cria uma instância de prova. Essa criação contém muita coisa implícita


for tag in inst.tags.listaTags:
	print(f'O tipo da tag é {tag.tipoTag}, o id da tag é {tag.idTag}, o nome é {tag.nome}, o peso é {tag.pesoTag}.')





#for linha in planilhaDeControleDeSorteio.registro:
#	print(f'O numero do slot é {linha.slot.idSlot}, parte {linha.slot.parte}, posicao {linha.slot.posicao}, descricao {linha.slot.descricao} e o pool é {linha.slot.pool}')
	

#for l in slotsProva.listaSlots:
#	print(f'O id do slot é {l.idSlot}, a parte é {l.parte}, a posição é {l.posicao}, a descrição é {l.descricao} e o pool é {l.pool}.')

#for r in planilhasDePool[0].registros:
#	print(f'O registro número {r.idQuestao} contém as tags: ')
#	tags = 'As tags são: '
#	for t in r.listaTags:
#		tags = tags + '  ' + str(t)
#	
#	print(tags + '\n')
	

#print(f'O número do modelo é {planilhaDeControleDeSorteio.modelo}, a instância é ' + \
#	f'{planilhaDeControleDeSorteio.instancia} e o id do candidato é {planilhaDeControleDeSorteio.candidato}.')