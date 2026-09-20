"""[20] Caixeiro-viajante por força bruta: O(n!) na prática (livro, cap. 1)
Tema: Big O / Força bruta | Complexidade: O(n!) | Memória: O(n)
Palavras-chave: caixeiro viajante, travelling salesman, permutações, força bruta, fatorial, n!, itertools.permutations, inviável, explode, rotas

O que faz:
- Gera todas as rotas possíveis entre n cidades (permutações) e escolhe a mais curta.
- Mostra o número de rotas e o tempo para n = 4..9, evidenciando o crescimento fatorial.
- Estima quanto tempo levaria para 12, 15 e 20 cidades.

Perguntas prováveis:
P: Por que o caixeiro-viajante por força bruta é O(n!)?
R: Porque testa todas as ordens possíveis de visitar as n cidades, e há n! permutações (5 cidades -> 120 rotas; 10 -> 3.628.800).
P: O que acontece quando se acrescenta uma cidade?
R: O número de rotas é multiplicado por n: de 7 para 8 cidades o trabalho cresce 8 vezes. Por isso é inviável para n grande.
P: Qual é o algoritmo mais lento da tabela do livro?
R: O(n!). Com n = 16 e um computador de 10 operações por segundo, levaria cerca de 66 mil anos.
"""
import itertools
import math
import random
import time


def distancia(a, b):
    return math.dist(a, b)


def melhor_rota(cidades):
    origem = cidades[0]
    melhor, menor = None, float("inf")
    rotas = 0
    for perm in itertools.permutations(cidades[1:]):        # (n-1)! rotas saindo da origem
        rotas += 1
        rota = (origem,) + perm + (origem,)
        total = sum(distancia(rota[i], rota[i + 1]) for i in range(len(rota) - 1))
        if total < menor:
            melhor, menor = rota, total
    return melhor, menor, rotas


if __name__ == "__main__":
    random.seed(42)
    print(f"{'cidades':>8} {'rotas (n-1)!':>13} {'tempo (s)':>10} {'crescimento':>12}")
    print("-" * 48)
    anterior = None
    tempos = {}
    for n in range(4, 10):
        cidades = [(random.random() * 100, random.random() * 100) for _ in range(n)]
        inicio = time.perf_counter()
        _, _, rotas = melhor_rota(cidades)
        t = time.perf_counter() - inicio
        tempos[n] = t
        cresc = f"{t / anterior:.1f}x" if anterior else "-"
        print(f"{n:>8} {rotas:>13} {t:>10.4f} {cresc:>12}")
        anterior = t

    por_rota = tempos[9] / math.factorial(8)
    print("\nEstimativa com o mesmo custo por rota:")
    for n in (12, 15, 20):
        segundos = por_rota * math.factorial(n - 1)
        if segundos < 3600:
            texto = f"{segundos:.0f} s"
        elif segundos < 86400 * 365:
            texto = f"{segundos / 86400:.1f} dias"
        else:
            texto = f"{segundos / (86400 * 365.25):,.0f} anos".replace(",", ".")
        print(f"  {n} cidades: {math.factorial(n - 1):>22,} rotas -> {texto}".replace(",", "."))
