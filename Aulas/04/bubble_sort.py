import random
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuracao do teste
# ---------------------------------------------------------------------------
# Listas de exemplo do enunciado (n = 5)
MELHOR_CASO = [1, 2, 3, 4, 5]      # ja ordenada
MEDIO_CASO = [3, 5, 1, 4, 2]       # ordem aleatoria
PIOR_CASO = [5, 4, 3, 2, 1]        # ordem inversa



def bubble_sort(lista):
    lista_cpy = list(lista) #copia da lista
    count_troca = 0
    count_for = 0
    n = len(lista_cpy)
    ordenado = False
    passagem = 0

    # No maximo n-1 passagens: depois disso a lista so pode estar ordenada.
    while not ordenado and passagem < n - 1:
        ordenado = True #parto do principio que ha ordenacao
        # A cada passagem o maior elemento restante ja "subiu" para o fim,
        # entao a cauda ja esta ordenada e nao precisa ser comparada de novo.
        for idx in range(0, n - 1 - passagem):
            count_for += 1
            if lista_cpy[idx] > lista_cpy[idx+1]:
                lista_cpy[idx], lista_cpy[idx+1] = lista_cpy[idx+1], lista_cpy[idx] # Troca de posicao
                count_troca += 1
                ordenado = False
                print(lista_cpy)
        passagem += 1

    return lista_cpy, count_troca, count_for


print(bubble_sort(MEDIO_CASO))



# ---------------------------------------------------------------------------
# 1) BUBBLE SORT - O(n^2)
#    Compara pares VIZINHOS e troca quando estao fora de ordem.
#    A cada passagem o maior elemento "sobe" para o final da lista.
#    Se uma passagem inteira nao trocar nada, a lista ja esta ordenada e o
#    algoritmo para - foi o que o enunciado pediu: "repete as passagens ate
#    nao haver mais trocas".
# ---------------------------------------------------------------------------
def bubble_sortIA(lista_original):
    lista = list(lista_original)        # copia, para nao alterar a original
    comparacoes = 0
    trocas = 0
    n = len(lista)

    for passagem in range(n - 1):
        houve_troca = False

        # A cada passagem o fim da lista ja esta ordenado, entao olhamos um
        # elemento a menos: por isso o "- passagem".
        for i in range(n - 1 - passagem):
            comparacoes = comparacoes + 1               # contou uma comparacao
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                trocas = trocas + 1                     # contou uma troca
                houve_troca = True

        if not houve_troca:             # passagem sem nenhuma troca -> ordenada
            break

    return lista, trocas, comparacoes 


print(bubble_sortIA(MEDIO_CASO))