"""[03] Busca binária recursiva (dividir para conquistar)
Tema: Busca / Dividir para conquistar | Complexidade: O(log n) | Memória: pilha O(log n)
Palavras-chave: busca binária recursiva, dividir para conquistar, caso base, caso recursivo, metade, profundidade da pilha, livro 4.4

O que faz:
- Implementa a busca binária como recursão: caso base = intervalo vazio ou alvo no meio; caso recursivo = chamar a função em uma das metades.
- Imprime cada chamada com recuo proporcional à profundidade, para visualizar a pilha.

Perguntas prováveis:
P: Qual é o caso base e o caso recursivo da busca binária? (Livro, ex. 4.4)
R: Caso base: intervalo vazio (não achou) ou elemento do meio igual ao alvo (achou). Caso recursivo: descartar a metade que não pode conter o alvo e repetir a busca na outra metade.
P: Por que a busca binária é um exemplo de dividir para conquistar?
R: Porque reduz o problema a um subproblema do mesmo tipo com metade do tamanho, até chegar ao caso base.
P: Qual é a profundidade máxima da pilha nessa versão?
R: Cerca de log2 n chamadas empilhadas, uma por metade descartada. Para n = 10, no máximo 4.
P: A versão recursiva é mais rápida que a iterativa?
R: Não; faz os mesmos passos. A recursiva gasta pilha O(log n) e tem custo de chamada; a iterativa usa memória O(1). A recursiva é mais clara para mostrar o dividir para conquistar.
"""


def busca_binaria_rec(lista, alvo, baixo=0, alto=None, profundidade=0):
    if alto is None:
        alto = len(lista) - 1
    recuo = "  " * profundidade
    if baixo > alto:                       # caso base 1: intervalo vazio
        print(f"{recuo}[{baixo}..{alto}] vazio -> nao esta na lista")
        return None
    meio = (baixo + alto) // 2
    print(f"{recuo}[{baixo}..{alto}] meio={meio} valor={lista[meio]}")
    if lista[meio] == alvo:                # caso base 2: achou
        return meio
    if lista[meio] < alvo:                 # caso recursivo: metade da direita
        return busca_binaria_rec(lista, alvo, meio + 1, alto, profundidade + 1)
    return busca_binaria_rec(lista, alvo, baixo, meio - 1, profundidade + 1)   # metade da esquerda


if __name__ == "__main__":
    lista = [3, 8, 12, 19, 25, 31, 37, 42, 49, 56]
    for alvo in (37, 4):
        print(f"\nProcurando {alvo} em {lista}")
        r = busca_binaria_rec(lista, alvo)
        print("resultado:", r)
