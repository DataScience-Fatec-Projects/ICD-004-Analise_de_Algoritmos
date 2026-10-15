# grafo estacoes de metro
# vertice = estacao | aresta = trecho direto entre duas estacoes de baldeacao
# a linha fica no comentario, ao lado de cada vizinho (ela pertence a aresta, nao a estacao)
#
#                                                      Luz ----L11---- Brás
#                                                L4 /      \ L1     / L3
#                                                 /          \    /
# Jundiaí --L7-- Palmeiras-Barra Funda --L3-- República --L3-- Sé
#                                                 |            |
#                                                 L4           L1
#                                                 |            |
#                               Paulista-Consolação ---L2----- Paraíso
#
# Aeroporto-Guarulhos --L13-- Engenheiro Goulart   (isolado: sem a L12)
#
metro = {
    'Jundiaí': ['Palmeiras-Barra Funda'],                    # L7
    'Palmeiras-Barra Funda': ['Jundiaí','República'],
    'República': ['Palmeiras-Barra Funda','Luz','Sé','Paulista-Consolação'],
    'Luz': ['República','Brás','Sé'],
    'Brás': ['Luz','Sé'],
    'Paulista-Consolação': ['República','Paraíso'],
    'Paraíso': ['Paulista-Consolação','Sé']
}

print(metro)
