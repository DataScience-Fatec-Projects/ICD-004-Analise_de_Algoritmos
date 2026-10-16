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
    'Paraíso': ['Paulista-Consolação','Sé'],
    'Sé': ['Luz','Brás','República','Paraíso'],
    'Aeroporto-Guarulhos': ['Engenheiro Goulart'],
    'Engenheiro Goulart': ['Aeroporto-Guarulhos']
}

for estacao, vizinhos in metro.items():
    print(f"{estacao:<22} -> {', '.join(vizinhos)}")

# grau = tamanho da lista de vizinhos; cada aresta aparece nas duas pontas,
# entao soma dos graus = 2 x arestas (lema do aperto de maos)
soma_graus = sum(len(vizinhos) for vizinhos in metro.values())
total_arestas = soma_graus // 2

print(f"Total de vértices: {len(metro)}")
print(f"Soma dos graus:    {soma_graus}")
print(f"Total de arestas:  {total_arestas}")

# checagem de simetria: se A tem B como vizinho, B tem que ter A
RED_BOLD = "[1;31m"
RESET = "[0m"

ok = True
for estacao, vizinhos in metro.items():
    for vizinho in vizinhos:
        if vizinho not in metro:
            ok = False
            print(f"Vizinho {RED_BOLD}{vizinho}{RESET} (de {estacao}) sem chave própria.")
        elif estacao not in metro[vizinho]:
            ok = False
            print(f"Ligação só de um lado: {estacao} -> {RED_BOLD}{vizinho}{RESET}, "
                  f"mas {vizinho} não tem {estacao}.")

if ok:
    print("Simetria OK: todas as ligações aparecem nos dois sentidos.")
