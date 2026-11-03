# Comentado pela IA Gemini (2.5 Pro)

import heapq  # biblioteca para implementar a fila de prioridade (Min-Heap)
import math   # para usar 'infinito'

def dijkstra(grafo, origem, destino):
    """
    Implementa o algoritmo de Dijkstra para encontrar o caminho de menor custo.

    Args:
        grafo (dict): O grafo representado como um dicionário de dicionários.
                      Ex: {'A': {'B': 7, 'D': 9}, ...}
        origem (str): O nó de partida.
        destino (str): O nó de chegada.

    Returns:
        tuple: (distancia_minima, caminho_mais_curto)
    """

    # 1. Inicialização
    # Distâncias: Armazena a menor distância conhecida até cada nó
    distancias = {vertice: math.inf for vertice in grafo}
    distancias[origem] = 0

    # Predecessores: Armazena o nó anterior no caminho mais curto
    predecessores = {vertice: None for vertice in grafo}

    # Fila de Prioridade (Min-Heap): Armazena tuplas (distancia, vertice)
    # A prioridade é a distância, então o heappop() sempre extrai o de menor distância
    fila_prioridade = [(0, origem)]  # Começa com (distancia 0, nó origem)

    # 2. Iteração Principal
    while fila_prioridade:
        # Extrai o nó com a menor distância provisória
        distancia_atual, u = heapq.heappop(fila_prioridade)

        # Se a distância extraída for maior que a distância já conhecida,
        # significa que já encontramos um caminho mais curto para 'u', então ignoramos.
        if distancia_atual > distancias[u]:
            continue

        # Se chegamos ao destino, podemos parar e reconstruir o caminho
        if u == destino:
            break

        # 3. Relaxamento dos Vizinhos
        # Percorre todos os vizinhos (v) de 'u'
        for v, peso in grafo[u].items():
            nova_distancia = distancia_atual + peso

            # Se a nova distância é menor do que a distância registrada para 'v'
            if nova_distancia < distancias[v]:
                # Atualiza a distância e o predecessor
                distancias[v] = nova_distancia
                predecessores[v] = u

                # Adiciona ou atualiza 'v' na fila de prioridade
                heapq.heappush(fila_prioridade, (nova_distancia, v))

    # 4. Reconstrução do Caminho
    caminho = []
    atual = destino
    
    # Percorre os predecessores de trás para frente até chegar à origem
    while atual is not None:
        caminho.insert(0, atual)
        atual = predecessores[atual]

    # Verifica se o destino foi alcançado (se a distância é finita)
    if distancias[destino] == math.inf:
        return math.inf, "Caminho não encontrado"
    
    return distancias[destino], caminho


# Representação do Grafo (Lista de Adjacências usando dicionário)
# Note que o nosso grafo de exemplo era não-direcionado, então cada conexão
# deve ser listada duas vezes (ex: A->B e B->A)
grafo_exemplo = {
    'A': {'B': 7, 'D': 9},
    'B': {'A': 7, 'D': 1, 'E': 8},
    'C': {'E': 5, 'F': 4},
    'D': {'A': 9, 'B': 1, 'F': 10},
    'E': {'B': 8, 'C': 5, 'F': 6},
    'F': {'D': 10, 'C': 4, 'E': 6}
}

origem = 'A'
destino = 'C'

distancia_minima, caminho_final = dijkstra(grafo_exemplo, origem, destino)

print(f"Origem: {origem}")
print(f"Destino: {destino}")
print("-" * 30)
print(f"Distância Mínima: {distancia_minima}")
print(f"Caminho Mais Curto: {' -> '.join(caminho_final)}")