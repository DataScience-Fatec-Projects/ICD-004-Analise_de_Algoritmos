# BFS (busca em largura) para achar o caminho com menos trechos entre duas estacoes
# base: exemplo da aula (exemplo.py), com tres ajustes:
#   1) marca como visitado AO ENFILEIRAR, e nao ao tirar da fila
#      (no exemplo a mesma estacao pode entrar varias vezes na fila antes de ser visitada)
#   2) trata origem == destino e estacao que nao existe no grafo
#   3) devolve None quando nao existe caminho
from collections import deque

from q1_grafo import metro


def bfs_caminho_mais_curto(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return None                          # estacao fora do grafo
    if origem == destino:
        return [origem]                      # ja chegou, caminho de uma estacao so

    fila = deque([(origem, [origem])])       # cada item: (estacao atual, caminho ate ela)
    visitados = {origem}

    while fila:
        atual, caminho = fila.popleft()      # FIFO: sai primeiro quem esta mais perto da origem
        for vizinho in grafo[atual]:
            if vizinho in visitados:
                continue
            if vizinho == destino:
                return caminho + [vizinho]   # primeira vez que acha = menor numero de trechos
            visitados.add(vizinho)
            fila.append((vizinho, caminho + [vizinho]))

    return None                              # fila esvaziou sem achar: componentes separados


def mostrar(grafo, origem, destino):
    caminho = bfs_caminho_mais_curto(grafo, origem, destino)
    print(f"{origem} -> {destino}")
    if caminho is None:
        faltando = [e for e in (origem, destino) if e not in grafo]
        if faltando:
            print(f"   sem caminho: {', '.join(faltando)} não está no grafo\n")
        else:
            print("   sem caminho possível: as estações não estão ligadas\n")
    else:
        print(f"   {' → '.join(caminho)}")
        print(f"   {len(caminho)} estação(ões), {len(caminho) - 1} trecho(s)\n")


if __name__ == "__main__":
    testes = [
        ('Jundiaí', 'Paraíso'),                     # L7 -> L3 -> L1: duas baldeacoes
        ('Brás', 'Paulista-Consolação'),            # empate: varios caminhos de 3 trechos, a ordem da lista decide
        ('Luz', 'Sé'),                              # vizinhos diretos
        ('Jundiaí', 'Aeroporto-Guarulhos'),         # L13 isolada: nao existe caminho
        ('Sé', 'Sé'),                               # origem == destino
        ('Jundiaí', 'Tatuapé'),                     # estacao fora do recorte
    ]
    for origem, destino in testes:
        mostrar(metro, origem, destino)
