import time
from collections import deque


""" 
    Representação de cada estado do quebra-cabeça
"""


class EstadoQuebraCabeca:
    def __init__(self, estado, pai, movimento, profundidade, custo):
        self.estado = estado
        self.pai = pai
        self.movimento = movimento
        self.profundidade = profundidade
        self.custo = custo
        if self.estado:
            self.mapeamento = "".join(str(numeroEstado)
                                      for numeroEstado in self.estado)


""" 
    Funções auxiliares
"""

# Busca de outros vertices possiveis
def sub_vertices(vertice):
    global total_vertices_visitados
    total_vertices_visitados = total_vertices_visitados + 1

    proximos_caminhos_possiveis = []
    proximos_caminhos_possiveis.append(
        EstadoQuebraCabeca(
            movimento(vertice.estado, 1),
            vertice,
            1,
            vertice.profundidade + 1,
            vertice.custo + 1,
        )
    )
    proximos_caminhos_possiveis.append(
        EstadoQuebraCabeca(
            movimento(vertice.estado, 2),
            vertice,
            2,
            vertice.profundidade + 1,
            vertice.custo + 1,
        )
    )
    proximos_caminhos_possiveis.append(
        EstadoQuebraCabeca(
            movimento(vertice.estado, 3),
            vertice,
            3,
            vertice.profundidade + 1,
            vertice.custo + 1,
        )
    )
    proximos_caminhos_possiveis.append(
        EstadoQuebraCabeca(
            movimento(vertice.estado, 4),
            vertice,
            4,
            vertice.profundidade + 1,
            vertice.custo + 1,
        )
    )
    vertices = []
    for caminhos_realmente_possiveis in proximos_caminhos_possiveis:
        if caminhos_realmente_possiveis.estado != None:
            vertices.append(caminhos_realmente_possiveis)

    return vertices


# Calcula movimentos possiveis
def movimento(estado, direcao):
    global tamanho_lado_quebra_cabeca, total_pecas_quebra_cabeca

    novo_estado = estado[:]
    indice = novo_estado.index(0)

    # Para cima
    if direcao == 1:
        if indice not in range(0, tamanho_lado_quebra_cabeca):
            temp = novo_estado[indice - tamanho_lado_quebra_cabeca]
            novo_estado[indice -
                        tamanho_lado_quebra_cabeca] = novo_estado[indice]
            novo_estado[indice] = temp

            return novo_estado
        else:
            return None

    # Para baixo
    if direcao == 2:
        if indice not in range(
            total_pecas_quebra_cabeca - tamanho_lado_quebra_cabeca, total_pecas_quebra_cabeca
        ):

            temp = novo_estado[indice + tamanho_lado_quebra_cabeca]
            novo_estado[indice +
                        tamanho_lado_quebra_cabeca] = novo_estado[indice]
            novo_estado[indice] = temp

            return novo_estado
        else:
            return None

    # Para esquerda
    if direcao == tamanho_lado_quebra_cabeca:
        if indice not in range(0, total_pecas_quebra_cabeca, tamanho_lado_quebra_cabeca):
            temp = novo_estado[indice - 1]
            novo_estado[indice - 1] = novo_estado[indice]
            novo_estado[indice] = temp

            return novo_estado
        else:
            return None

    # Para direita
    if direcao == 4:
        if indice not in range(
            tamanho_lado_quebra_cabeca - 1, total_pecas_quebra_cabeca, tamanho_lado_quebra_cabeca
        ):
            temp = novo_estado[indice + 1]
            novo_estado[indice + 1] = novo_estado[indice]
            novo_estado[indice] = temp

            return novo_estado
        else:
            return None


""" 
    Funções de busca cega
"""


# Busca em largura
def busca_largura(estado_inicial):
    global largura_maxima, vertice_solucao, profundidade_maxima

    fila = deque([EstadoQuebraCabeca(estado_inicial, None, None, 0, 0)])
    vertice_visitado = set()

    while fila:
        vertice = fila.popleft()
        vertice_visitado.add(vertice.mapeamento)
        if vertice.estado == solucao_desejada:
            vertice_solucao = vertice
            return fila

        caminhos_possiveis = sub_vertices(vertice)
        for caminho in caminhos_possiveis:
            if caminho.mapeamento not in vertice_visitado:
                fila.append(caminho)
                vertice_visitado.add(caminho.mapeamento)
                if caminho.profundidade > profundidade_maxima:
                    profundidade_maxima = profundidade_maxima + 1
        if len(fila) > largura_maxima:
            largura_maxima = len(fila)


# Busca em profundidade
def busca_profundidade(estado_inicial):
    global largura_maxima, vertice_solucao, profundidade_maxima

    vertice_visitado = set()
    pilha = list([EstadoQuebraCabeca(estado_inicial, None, None, 0, 0)])

    while pilha:
        vertice = pilha.pop()
        vertice_visitado.add(vertice.mapeamento)
        if vertice.estado == solucao_desejada:
            vertice_solucao = vertice
            return pilha

        caminhos_possiveis = sub_vertices(vertice)
        for caminho in caminhos_possiveis:
            if caminho.mapeamento not in vertice_visitado:
                pilha.append(caminho)
                vertice_visitado.add(caminho.mapeamento)
                if caminho.profundidade > profundidade_maxima:
                    profundidade_maxima = 1 + profundidade_maxima
        if len(pilha) > largura_maxima:
            largura_maxima = len(pilha)


""" 
    Função de busca heurística
"""

# Ordenação de listas por argumento
def ordena_por_prioridade(lista):
    return lista["prioridade"]


# Busca gulosa
def busca_gulosa(estado_inicial, heuristica):
    global largura_maxima, vertice_solucao, profundidade_maxima

    prioridade = (
        heuristica_pecas_fora_do_lugar(estado_inicial, solucao_desejada)
        if heuristica == "1"
        else heuristica_manhattan(estado_inicial, solucao_desejada)
    )

    vertice_visitado = set()
    lista_ordenada = [
        {
            "prioridade": prioridade,
            "estado": EstadoQuebraCabeca(estado_inicial, None, None, 0, 0),
        }
    ]

    lista_ordenada.sort(key=ordena_por_prioridade)

    while lista_ordenada:
        vertice = lista_ordenada.pop()
        vertice_visitado.add(vertice["estado"].mapeamento)
        if vertice["estado"].estado == solucao_desejada:
            vertice_solucao = vertice["estado"]
            return lista_ordenada[:][-1]

        caminhos_possiveis = sub_vertices(vertice["estado"])

        prioridades_caminhos_possiveis = [
            heuristica_pecas_fora_do_lugar(
                estado_atual.estado, solucao_desejada)
            if heuristica == "1"
            else heuristica_manhattan(estado_atual.estado, solucao_desejada)
            for estado_atual in caminhos_possiveis
        ]

        caminhos_possiveis_ordenados = [
            {"prioridade": prioridade, "estado": estado}
            for prioridade, estado in zip(
                prioridades_caminhos_possiveis, caminhos_possiveis
            )
        ]
        caminhos_possiveis_ordenados.sort(key=ordena_por_prioridade)

        for caminho in caminhos_possiveis_ordenados:
            if caminho["estado"].mapeamento not in vertice_visitado:
                lista_ordenada.append(caminho)
                vertice_visitado.add(caminho["estado"].mapeamento)
                if caminho["estado"].profundidade > profundidade_maxima:
                    profundidade_maxima = 1 + profundidade_maxima
        if len(lista_ordenada) > largura_maxima:
            largura_maxima = len(lista_ordenada)


# Heurística 1: considera a quantidade de peças que estão fora do lugar
def heuristica_pecas_fora_do_lugar(estado_atual, estado_desejado):
    pecas_fora_do_lugar = 0

    for i in range(len(estado_atual)):
        pecas_fora_do_lugar += 1 if estado_atual[i] != estado_desejado[i] else 0

    return pecas_fora_do_lugar


# Heurística 2: cálculo da distância Manhattan
def heuristica_manhattan(estado_atual, estado_desejado):
    global tamanho_lado_quebra_cabeca, total_pecas_quebra_cabeca

    distancia = sum(
        abs(atual % tamanho_lado_quebra_cabeca - desejado %
            tamanho_lado_quebra_cabeca)
        + abs(atual // tamanho_lado_quebra_cabeca -
              desejado // tamanho_lado_quebra_cabeca)
        for atual, desejado in (
            (estado_atual.index(i), estado_desejado.index(i))
            for i in range(1, total_pecas_quebra_cabeca)
        )
    )

    return distancia


# Formatador de impressão
def imprime_tabuleiro(estado_atual):
    for linha in range(total_pecas_quebra_cabeca):
        print(estado_atual[linha], sep=' ', end='', flush=True)
        if linha % 3 == 2:
            print('')


""" 
    Valores iniciais
"""
estado_inicial = [0, 1, 2, 7, 8, 3, 6, 5, 4]
solucao_desejada = [1, 2, 3, 8, 0, 4, 7, 6, 5]
vertice_solucao = None

tempo_inicial = 0
tempo_final = 0

total_pecas_quebra_cabeca = len(estado_inicial)
tamanho_lado_quebra_cabeca = int(total_pecas_quebra_cabeca ** 0.5)
total_vertices_visitados = 0
profundidade_maxima = 0
largura_maxima = 0

""" 
    Operação do script
"""
print("Escolha qual tipo de busca usar:")
print("1 - Busca cega")
print("2 - Busca heurística")
algoritmo = input("Digite um numero: ")

if algoritmo == "1":
    print("\n\nEscolha qual algoritmo de busca cega usar:")
    print("1 - Busca em largura")
    print("2 - Busca em profundidade")
    busca = input("Digite um numero: ")

    tempo_inicial = time.time()

    if busca == "1":
        busca_largura(
            estado_inicial)
    elif busca == "2":
        busca_profundidade(
            estado_inicial)

    tempo_final = time.time()

elif algoritmo == "2":
    print("\n\nO algoritmo heurístico de busca gulosa será usado.")

    print("\n\nEscolha a heurística:")
    print("1 - Número de peças fora do lugar")
    print("2 - Distância Manhattan")
    heuristica = input("Digite um numero: ")

    tempo_inicial = time.time()

    busca_gulosa(estado_inicial, heuristica)

    tempo_final = time.time()

elif algoritmo != "1":
    print("Essa opção não existe. Encerrando agora...")
    exit()

profundidade = vertice_solucao.profundidade
estado_final = vertice_solucao.estado
movimentos = []
while estado_inicial != vertice_solucao.estado:
    if vertice_solucao.movimento == 1:
        caminho = "CIMA"
    if vertice_solucao.movimento == 2:
        caminho = "BAIXO"
    if vertice_solucao.movimento == 3:
        caminho = "ESQUERDA"
    if vertice_solucao.movimento == 4:
        caminho = "DIREITA"
    movimentos.insert(0, caminho)
    vertice_solucao = vertice_solucao.pai

tempo_total = tempo_final - tempo_inicial

print("\n\nRESULTADO:")
print("###########")
print("Movimentos:", movimentos)
print("A resolução tem ", len(movimentos), " passos.")
print("----------")
print("Tabuleiro inicial:")
imprime_tabuleiro(estado_inicial)
print("----------")
print("Tabuleiro final:")
imprime_tabuleiro(estado_final)
print("----------")
print("Total de vértices visitados:", str(total_vertices_visitados))
print("Profundidade da resposta:", str(profundidade))
print("Profundidade máxima alcancada:", str(profundidade_maxima))
print("Largura máxima alcancada:", str(largura_maxima))
print("Tempo total de execução:", str(tempo_total), "s")
