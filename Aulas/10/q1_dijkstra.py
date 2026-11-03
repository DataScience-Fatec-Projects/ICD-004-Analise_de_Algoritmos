# Atividade 07 - questao 1
# Dijkstra com e sem Min-Heap:
#   dijkstra          -> implementacao da aula (dijkstra_heap.py), com heapq    O((V + E) log V)
#   dijkstra_sem_heap -> a mesma funcao, escolhendo o proximo no por varredura  O(V^2)
import contextlib
import io
import math
import random
import time
from math import inf

with contextlib.redirect_stdout(io.StringIO()):     # o arquivo da aula imprime o exemplo dele ao ser importado
    from dijkstra_heap import dijkstra, grafo_exemplo

# grafo do metro da atividade 06, agora PONDERADO
# peso = tempo aproximado de viagem em minutos (sem contar o tempo de baldeacao)
# dicionario de dicionarios: metro_min[a][b] = minutos para ir de a ate b
metro_min = {
    'Jundiaí':               {'Palmeiras-Barra Funda': 70},                                   # L7
    'Palmeiras-Barra Funda': {'Jundiaí': 70, 'República': 6},
    'República':             {'Palmeiras-Barra Funda': 6, 'Luz': 2, 'Sé': 3, 'Paulista-Consolação': 4},
    'Luz':                   {'República': 2, 'Brás': 4, 'Sé': 3},
    'Brás':                  {'Luz': 4, 'Sé': 4},
    'Paulista-Consolação':   {'República': 4, 'Paraíso': 5},
    'Paraíso':               {'Paulista-Consolação': 5, 'Sé': 7},
    'Sé':                    {'Luz': 3, 'Brás': 4, 'República': 3, 'Paraíso': 7},
    'Aeroporto-Guarulhos':   {'Engenheiro Goulart': 9},                                       # L13
    'Engenheiro Goulart':    {'Aeroporto-Guarulhos': 9},
}


def fmt(x):
    """Mostra infinito como o simbolo, e numeros sem casas decimais inuteis."""
    return '∞' if x == inf else f'{x:g}'


def custo(grafo, trajeto):
    """Soma dos pesos das arestas de um caminho."""
    return sum(grafo[a][b] for a, b in zip(trajeto, trajeto[1:]))


def milhar(n):
    """Inteiro com espaco separando os milhares: 3996001 -> '3 996 001'."""
    return f"{n:,}".replace(",", " ")


def dijkstra_sem_heap(grafo, origem, destino):
    """
    A mesma implementação da aula (dijkstra_heap.py), trocando o Min-Heap por uma varredura.
    Mesma assinatura e mesmo retorno: (distancia_minima, caminho_mais_curto).
    Os trechos que mudaram estão marcados com  >>> SEM HEAP
    """

    # 1. Inicialização
    distancias = {vertice: math.inf for vertice in grafo}
    distancias[origem] = 0
    predecessores = {vertice: None for vertice in grafo}

    # >>> SEM HEAP: no lugar da fila de prioridade, um conjunto com os nós já processados
    visitados = set()

    # 2. Iteração Principal
    # >>> SEM HEAP: no máximo uma volta por vértice
    while len(visitados) < len(grafo):
        # >>> SEM HEAP: extrai o nó com a menor distância provisória VARRENDO todos -> O(V)
        u = None
        for vertice in grafo:
            if vertice not in visitados and (u is None or distancias[vertice] < distancias[u]):
                u = vertice
        if distancias[u] == math.inf:
            break                                # os que sobraram não são alcançáveis
        visitados.add(u)
        distancia_atual = distancias[u]

        # Se chegamos ao destino, podemos parar e reconstruir o caminho
        if u == destino:
            break

        # 3. Relaxamento dos Vizinhos
        for v, peso in grafo[u].items():
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                predecessores[v] = u
                # >>> SEM HEAP: sem heappush; a próxima varredura já enxerga a nova distância

    # 4. Reconstrução do Caminho (igual)
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = predecessores[atual]

    if distancias[destino] == math.inf:
        return math.inf, "Caminho não encontrado"

    return distancias[destino], caminho


def grafo_aleatorio(n, saidas_por_vertice, semente=42):
    """Grafo direcionado com pesos de 1 a 100. O anel i -> i+1 garante que todos sao alcancaveis."""
    rng = random.Random(semente)
    grafo = {v: {} for v in range(n)}
    for u in range(n):
        grafo[u][(u + 1) % n] = rng.randint(1, 100)
        for v in rng.sample(range(n), min(saidas_por_vertice, n - 1)):
            if v != u:
                grafo[u][v] = rng.randint(1, 100)
    return grafo


def cronometrar(funcao, *argumentos, repeticoes=3):
    """Melhor tempo (em ms) entre algumas execucoes, para reduzir o ruido do sistema."""
    melhor = inf
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao(*argumentos)
        melhor = min(melhor, time.perf_counter() - inicio)
    return melhor * 1000


def comparar(tamanhos, saidas):
    """Mede as duas versoes em grafos de tamanho crescente e confere se dao a mesma resposta."""
    print(f"{'V':>6} {'E':>9} {'sem heap (ms)':>14} {'com heap (ms)':>14} {'razão':>8}")
    linhas = []
    for n in tamanhos:
        g = grafo_aleatorio(n, saidas(n))
        e = sum(len(viz) for viz in g.values())
        for destino in random.Random(n).sample(range(n), 3):      # confere 3 destinos sorteados
            assert dijkstra_sem_heap(g, 0, destino)[0] == dijkstra(g, 0, destino)[0]
        g[n] = {}      # destino isolado: nunca e alcancado, entao as duas versoes processam o grafo todo
        t_sem, t_com = cronometrar(dijkstra_sem_heap, g, 0, n), cronometrar(dijkstra, g, 0, n)
        linhas.append((n, e, t_sem, t_com))
        print(f"{milhar(n):>6} {milhar(e):>9} {t_sem:>14.1f} {t_com:>14.1f} {t_sem / t_com:>7.1f}x")
    return linhas


if __name__ == "__main__":
    # 1) grafo de exemplo da aula: de A ate cada vertice, nas duas versoes
    print(f"{'A até':<6} {'sem heap':>8} {'com heap':>8}   caminho (com heap)")
    for destino in grafo_exemplo:
        d_sem, _ = dijkstra_sem_heap(grafo_exemplo, 'A', destino)
        d_com, rota = dijkstra(grafo_exemplo, 'A', destino)
        assert d_sem == d_com                        # as duas versoes tem que concordar
        print(f"{destino:<6} {fmt(d_sem):>8} {fmt(d_com):>8}   {' → '.join(rota)}")

    # 2) metro: de Jundiai ate cada estacao
    resultados = []
    for estacao in metro_min:
        d_sem, _ = dijkstra_sem_heap(metro_min, 'Jundiaí', estacao)
        d_com, rota = dijkstra(metro_min, 'Jundiaí', estacao)
        assert d_sem == d_com
        resultados.append((d_com, estacao, d_sem, rota))

    print(f"\n{'Jundiaí até':<22} {'sem heap':>8} {'com heap':>8}   caminho (com heap)")
    for d_com, estacao, d_sem, rota in sorted(resultados, key=lambda r: r[0]):
        texto = ' → '.join(rota) if d_com < inf else rota        # rota = "Caminho não encontrado"
        print(f"{estacao:<22} {fmt(d_sem):>8} {fmt(d_com):>8}   {texto}")

    rota_bfs = ['Jundiaí', 'Palmeiras-Barra Funda', 'República', 'Sé', 'Paraíso']   # resposta da BFS (atividade 06)
    _, rota_dij = dijkstra(metro_min, 'Jundiaí', 'Paraíso')
    print("\nJundiaí → Paraíso")
    print(f"  BFS      (menos trechos): {' → '.join(rota_bfs)}  = {len(rota_bfs) - 1} trechos, {custo(metro_min, rota_bfs)} min")
    print(f"  Dijkstra (menos tempo):   {' → '.join(rota_dij)}  = {len(rota_dij) - 1} trechos, {custo(metro_min, rota_dij)} min")

    print("\nESPARSO (cerca de 6 arestas saindo de cada vértice)")
    comparar([250, 500, 1000, 2000, 4000], lambda n: 5)
    print("\nDENSO (cada vértice ligado a todos os outros)")
    comparar([100, 200, 400, 800], lambda n: n - 1)
