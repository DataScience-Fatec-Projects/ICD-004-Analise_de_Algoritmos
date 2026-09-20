"""[01] Busca linear com contagem de passos
Tema: Busca | Complexidade: melhor O(1), médio e pior O(n) | Memória: O(1)
Palavras-chave: busca linear, busca sequencial, passos, pior caso, melhor caso, caso médio, alvo ausente, lista desordenada, for

O que faz:
- Percorre a lista item a item até achar o alvo, contando quantos itens olhou.
- Mostra os quatro cenários: alvo na 1ª posição (melhor), no meio (médio), no fim e ausente (pior).
- Mostra que, quando n dobra, o pior caso dobra (crescimento linear).

Perguntas prováveis:
P: Qual é a complexidade da busca linear no pior caso e por quê?
R: O(n). No pior caso (alvo na última posição ou ausente) ela compara o alvo com todos os n elementos.
P: A busca linear exige lista ordenada?
R: Não. Funciona em qualquer lista; essa é a vantagem dela sobre a busca binária.
P: Quantos passos no melhor caso? E no caso médio?
R: Melhor: 1 passo (alvo na 1ª posição), O(1). Médio: cerca de n/2 passos, que continua sendo O(n) porque a constante 1/2 é ignorada.
P: Se a lista dobrar de tamanho, o que acontece com o pior caso?
R: Dobra também: 1.000 elementos -> 1.000 passos; 2.000 -> 2.000 passos. É a marca do crescimento linear.
"""


def busca_linear(lista, alvo):
    """Devolve (indice ou None, passos)."""
    passos = 0
    for i in range(len(lista)):
        passos += 1                       # olhou mais um elemento
        if lista[i] == alvo:
            return i, passos
    return None, passos                   # percorreu tudo e nao achou


if __name__ == "__main__":
    n = 1000
    lista = list(range(0, 2 * n, 2))      # 0, 2, 4, ... (n numeros pares, ordenados)
    cenarios = [
        ("melhor caso (1a posicao)", lista[0]),
        ("caso medio (meio)", lista[n // 2]),
        ("pior caso (ultimo)", lista[-1]),
        ("pior caso (ausente)", 1),        # impar: nao esta na lista
    ]
    print(f"BUSCA LINEAR em lista de {n} elementos")
    print("-" * 62)
    for nome, alvo in cenarios:
        idx, passos = busca_linear(lista, alvo)
        print(f"{nome:<27} alvo={alvo:<6} indice={str(idx):<6} passos={passos}")

    print("\nQuando n dobra, o pior caso dobra (O(n)):")
    for n2 in (1000, 2000, 4000, 8000):
        _, p = busca_linear(list(range(n2)), -1)
        print(f"  n={n2:<6} passos no pior caso={p}")
