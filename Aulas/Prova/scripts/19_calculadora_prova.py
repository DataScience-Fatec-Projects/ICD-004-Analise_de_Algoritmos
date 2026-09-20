"""[19] Calculadora para a prova: passos da busca binária, n(n-1)/2, Fibonacci, chamadas, potências de 2
Tema: Ferramenta / Big O | Complexidade: — | Memória: —
Palavras-chave: calculadora, log2, potências de 2, ceil, floor, n(n-1)/2, fibonacci, 2F(n+1)-1, 2n-1, fatorial, tabela, estimar tempo, quanto tempo leva

O que faz:
- Para um n dado (argumento na linha de comando ou os exemplos padrão) imprime: passos da busca binária (livro e implementação), comparações de selection/bubble no pior caso, n·log2 n, n², 2^n e n!.
- Imprime F(n) e o número de chamadas do Fibonacci recursivo puro e memoizado.
- Estima o tempo para um n maior a partir de um tempo medido e da classe de complexidade.
Uso: python 19_calculadora_prova.py 240000

Perguntas prováveis:
P: Quantos passos a busca binária faz para n = 240.000? E para 4 bilhões?
R: ceil(log2 240.000) = 18; ceil(log2 4.000.000.000) = 32.
P: Quantas comparações faz o selection sort para n = 1.000?
R: n(n-1)/2 = 499.500.
P: Um algoritmo O(n²) leva 2 s para n = 1.000; quanto leva para n = 10.000?
R: n cresceu 10x, trabalho 100x: cerca de 200 s. Se fosse O(n log n): cerca de 13x, ~27 s.
P: Quantas chamadas faz fib_recursivo(25)? E fib_memo(25)?
R: 2·F(26) − 1 = 242.785 e 2·25 − 1 = 49.
"""
import math
import sys


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def estimar(tempo_medido, n_medido, n_novo, classe):
    f = {
        "O(1)": lambda n: 1, "O(log n)": math.log2, "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n), "O(n^2)": lambda n: n ** 2, "O(2^n)": lambda n: 2 ** n,
    }[classe]
    return tempo_medido * f(n_novo) / f(n_medido)


def br(x):
    return f"{x:,.0f}".replace(",", ".")


def fmt(x):
    return br(x) if x < 1e12 else f"{x:.2e}"


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or [100, 128, 1_000, 240_000, 1_000_000, 4_000_000_000]
    print(f"{'n':>14} {'bin. livro':>10} {'bin. impl.':>10} {'n(n-1)/2':>22} {'n*log2 n':>14}")
    print("-" * 76)
    for n in ns:
        print(f"{br(n):>14} {math.ceil(math.log2(n)):>10} {math.floor(math.log2(n)) + 1:>10} {fmt(n * (n - 1) // 2):>22} {fmt(n * math.log2(n)):>14}")
    print("bin. livro = ceil(log2 n) | bin. impl. = floor(log2 n)+1 (conta a comparacao final)")

    print(f"\n{'n':>3} {'F(n)':>10} {'chamadas rec. puro':>19} {'chamadas memo':>14} {'n!':>18} {'2^n':>13}")
    for n in (5, 10, 15, 20, 25, 30):
        print(f"{n:>3} {br(fib(n)):>10} {br(2 * fib(n + 1) - 1):>19} {2 * n - 1:>14} {br(math.factorial(n)) if n <= 15 else '> 10^18':>18} {br(2 ** n):>13}")

    print("\nPotencias de 2:")
    print("  " + "  ".join(f"2^{k}={br(2 ** k)}" for k in range(1, 21)))

    print("\nEstimativa: O(n^2) leva 2 s para n = 1.000. Para n = 10.000:")
    for classe in ("O(n)", "O(n log n)", "O(n^2)"):
        print(f"  se fosse {classe:<10}: {estimar(2, 1_000, 10_000, classe):>8.1f} s")
