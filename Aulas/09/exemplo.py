#Aula gravada em:
#youtu.be/XRFNhU-1y1c
from collections import deque

def bfs_caminho_mais_curto(grafo, origem, destino):
    fila = deque()
    fila.append((origem, [origem]))  # Guarda o caminho percorrido
    visitados = set()

    while fila:
        atual, caminho = fila.popleft()
        if atual == destino:
            return caminho  # Caminho mais curto encontrado
        if atual not in visitados:
            visitados.add(atual)
            for vizinho in grafo.get(atual, []):
                fila.append((vizinho, caminho + [vizinho]))
    return None  # Não existe caminho

# exemplo de grafo
rede_colaborativa = {
    'Ana': {'Bruno', 'Carla'},
    'Bruno': {'Ana', 'Daniel'},
    'Carla': {'Ana', 'Daniel'},
    'Daniel': {'Bruno', 'Carla', 'Eduarda'},
    'Eduarda': {'Daniel'}
}

# Busca caminho mais curto de 'Ana' até 'Eduarda'
caminho = bfs_caminho_mais_curto(rede_colaborativa, 'Ana', 'Eduarda')
print(caminho)  # Exemplo de saída: ['Ana', 'Bruno', 'Daniel', 'Eduarda']
