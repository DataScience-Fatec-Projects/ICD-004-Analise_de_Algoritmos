# Atividade 07 - questao 2
# Bellman-Ford: menor caminho aceitando pesos negativos, com deteccao de ciclo negativo
#   ate V - 1 rodadas relaxando TODAS as arestas + 1 rodada de checagem   O(V * E)
from math import inf

from q1_dijkstra import dijkstra, fmt

def arestas_de(grafo):
    """Converte o dicionario de dicionarios em lista de arestas (u, v, peso)."""
    return [(u, v, peso) for u in grafo for v, peso in grafo[u].items()]


def remontar_caminho(predecessores, destino):
    """Volta pelos predecessores, do destino ate a origem (a etapa 4 do Dijkstra da aula)."""
    caminho = []
    while destino is not None:
        caminho.append(destino)
        destino = predecessores[destino]
    return caminho[::-1]


def extrair_ciclo(predecessores, v, n):
    """Volta n passos pelos predecessores (assim cai com certeza dentro do ciclo) e recolhe o ciclo."""
    for _ in range(n):
        v = predecessores[v]
    ciclo = [v]
    u = predecessores[v]
    while u != v:
        ciclo.append(u)
        u = predecessores[u]
    ciclo.append(v)
    return ciclo[::-1]                           # na ordem em que as arestas sao percorridas


def bellman_ford(vertices, arestas, origem, mostrar=False):
    """Menor custo da origem ate cada vertice, aceitando pesos negativos.
    Devolve (distancias, predecessores, ciclo, rodadas); ciclo = None quando nao ha ciclo negativo."""
    # 1) inicializacao: igual a do Dijkstra
    distancias = {v: inf for v in vertices}
    predecessores = {v: None for v in vertices}
    distancias[origem] = 0

    # 2) ate V - 1 rodadas; em cada uma, tenta relaxar TODAS as arestas
    rodadas, mudou = 0, False
    for rodada in range(1, len(vertices)):
        rodadas, mudou = rodada, False
        if mostrar:
            print(f"Rodada {rodada}")
        for u, v, peso in arestas:
            rotulo = f"{u}→{v} ({peso:+g})"
            if distancias[u] == inf:             # u ainda nao foi alcancado: nao tem o que propagar
                if mostrar:
                    print(f"  {rotulo:<11} {u} = ∞, ainda não alcançado: pula")
                continue
            nova_distancia = distancias[u] + peso
            conta = f"{fmt(distancias[u])} {'+' if peso >= 0 else '-'} {fmt(abs(peso))} = {fmt(nova_distancia)}"
            if nova_distancia < distancias[v]:   # relaxamento: passar por u ficou mais barato
                if mostrar:
                    print(f"  {rotulo:<11} {conta} < {fmt(distancias[v])}  → {v} = {fmt(nova_distancia)}")
                distancias[v] = nova_distancia
                predecessores[v] = u
                mudou = True
            elif mostrar:
                print(f"  {rotulo:<11} {conta}, não melhora {v} = {fmt(distancias[v])}")
        if mostrar:
            print("  distâncias:", "  ".join(f"{x}={fmt(distancias[x])}" for x in vertices))
        if not mudou:                            # rodada inteira sem mudanca: ja convergiu
            if mostrar:
                print("  nenhuma mudança nesta rodada: pode parar antes do limite")
            break
    if mostrar and mudou:
        print(f"limite de V - 1 = {len(vertices) - 1} rodadas atingido")

    # 3) checagem: se alguma aresta AINDA melhora, existe ciclo negativo
    for u, v, peso in arestas:
        if distancias[u] != inf and distancias[u] + peso < distancias[v]:
            if mostrar:
                print(f"Checagem: {u}→{v} ainda melhora: existe ciclo negativo")
            predecessores[v] = u
            return distancias, predecessores, extrair_ciclo(predecessores, v, len(vertices)), rodadas
    if mostrar:
        print("Checagem: nenhuma aresta melhora mais, então não há ciclo negativo")
    return distancias, predecessores, None, rodadas


if __name__ == "__main__":
    # 1) o grafo que engana o Dijkstra
    grafo_neg = {'A': {'B': 2, 'C': 5}, 'B': {'D': 1}, 'C': {'B': -4}, 'D': {}}
    print("Dijkstra da aula, A -> D:", dijkstra(grafo_neg, 'A', 'D'))
    distancias, predecessores, _, _ = bellman_ford(list(grafo_neg), arestas_de(grafo_neg), 'A')
    print("Bellman-Ford,     A -> D:", (distancias['D'], remontar_caminho(predecessores, 'D')))

    # 2) exemplo passo a passo
    print()
    vertices = ['A', 'B', 'C', 'D', 'E']
    # ordem "de tras para frente" de proposito: e o pior caso para este grafo
    arestas = [
        ('D', 'E', -4),
        ('C', 'D', 3),
        ('E', 'C', 2),
        ('B', 'C', -2),
        ('B', 'E', 6),
        ('A', 'B', 4),
        ('A', 'C', 5),
        ('A', 'D', 8),
    ]
    distancias, predecessores, ciclo, rodadas = bellman_ford(vertices, arestas, 'A', mostrar=True)
    for v in vertices:
        print(f"{v}: {fmt(distancias[v]):>3}  {' → '.join(remontar_caminho(predecessores, v))}")

    # 3) ciclo negativo
    arestas_c = [('A', 'B', 1), ('B', 'C', 3), ('C', 'D', 2), ('D', 'B', -6), ('D', 'E', 1)]
    print("\nciclo negativo:", bellman_ford(list('ABCDE'), arestas_c, 'A')[2])
