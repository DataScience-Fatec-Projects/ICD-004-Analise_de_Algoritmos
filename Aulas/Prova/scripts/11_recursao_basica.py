"""[11] Recursão básica: soma, contagem, máximo, fatorial e contagem regressiva (com profundidade da pilha)
Tema: Recursividade | Complexidade: O(n) chamadas | Memória: pilha O(n)
Palavras-chave: recursão, caso base, caso recursivo, soma recursiva, contar, máximo, fatorial, regressiva, profundidade da pilha, RecursionError, stack overflow, livro 4.1 4.2 4.3

O que faz:
- Implementa as funções recursivas do livro/aula (soma, contar, máximo, fatorial, contagem regressiva) mostrando cada chamada com recuo.
- Mede a profundidade máxima da pilha.
- Demonstra o que acontece sem caso base: captura o RecursionError.

Perguntas prováveis:
P: O que são caso base e caso recursivo?
R: Caso base: condição em que a função devolve a resposta sem chamar a si mesma (lista vazia, n <= 1). Caso recursivo: a função chama a si mesma com um problema menor, aproximando-se do caso base.
P: O que acontece se esquecer o caso base? (Livro, ex. 3.2)
R: A função nunca para; a pilha cresce até estourar. Em Python: RecursionError: maximum recursion depth exceeded (limite padrão ~1.000).
P: Qual é a profundidade da pilha em soma([2, 4, 6])?
R: 4 quadros ao mesmo tempo: soma([2,4,6]), soma([4,6]), soma([6]) e soma([]). Para n elementos: n + 1 chamadas, O(n) tempo e O(n) de pilha.
P: Em que ordem o fatorial multiplica?
R: De baixo para cima: só depois de chegar ao caso base fatorial(1) = 1 é que 2*1, 3*2, 4*6 e 5*24 = 120 são calculados nos retornos.
"""
import sys

profundidade_atual = 0
profundidade_maxima = 0


def entrar(texto):
    global profundidade_atual, profundidade_maxima
    print("  " * profundidade_atual + texto)
    profundidade_atual += 1
    profundidade_maxima = max(profundidade_maxima, profundidade_atual)


def sair():
    global profundidade_atual
    profundidade_atual -= 1


def soma(lista):                              # livro ex. 4.1 / aula 06
    entrar(f"soma({lista})")
    if lista == []:                           # caso base
        sair(); return 0
    r = lista[0] + soma(lista[1:])            # caso recursivo
    sair(); return r


def contar(lista):                            # livro ex. 4.2
    if lista == []:
        return 0
    return 1 + contar(lista[1:])


def maximo(lista):                            # livro ex. 4.3
    if len(lista) == 1:                       # caso base: 1 elemento
        return lista[0]
    resto = maximo(lista[1:])
    return lista[0] if lista[0] > resto else resto


def fatorial(n):                              # livro cap. 3
    entrar(f"fatorial({n})")
    if n <= 1:
        sair(); return 1
    r = n * fatorial(n - 1)
    print("  " * (profundidade_atual - 1) + f"-> {n} * fatorial({n - 1}) = {r}")
    sair(); return r


def regressiva(i):                            # livro cap. 3
    print(i, end=" ")
    if i <= 1:                                # caso base
        print()
        return
    regressiva(i - 1)


def sem_caso_base(n):
    return sem_caso_base(n + 1)               # nunca para!


if __name__ == "__main__":
    print("soma([2, 4, 6]):")
    print("  resultado =", soma([2, 4, 6]), "| profundidade maxima da pilha =", profundidade_maxima)

    print("\ncontar([7, 8, 9, 10]) =", contar([7, 8, 9, 10]))
    print("maximo([3, 9, 2, 7]) =", maximo([3, 9, 2, 7]))

    profundidade_maxima = 0
    print("\nfatorial(5):")
    print("  resultado =", fatorial(5), "| profundidade maxima da pilha =", profundidade_maxima)

    print("\nregressiva(5):")
    regressiva(5)

    print("\nSem caso base (limite de recursao =", sys.getrecursionlimit(), "):")
    try:
        sem_caso_base(1)
    except RecursionError as erro:
        print("  RecursionError:", erro)
