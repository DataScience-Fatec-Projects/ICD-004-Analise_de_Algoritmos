"""[18] Como medir tempo sem se enganar: perf_counter, timeit, mediana x média, seed e validação
Tema: Medição / Benchmark | Complexidade: — | Memória: —
Palavras-chave: perf_counter, time.time, timeit, repeat, mediana, média, mínimo, pico, ruído, random.seed, reprodutibilidade, assert, validar corretude, benchmark honesto, statistics

O que faz:
- Mostra a diferença entre time.time e time.perf_counter (resolução).
- Simula medições com um pico de sistema operacional e compara média, mediana e mínimo.
- Mostra random.seed garantindo os mesmos sorteios e a validação com assert antes de comparar dois algoritmos.

Perguntas prováveis:
P: Por que repetir a medição e usar mediana ou mínimo?
R: Uma medição isolada de microssegundos fica no ruído do relógio; a média é puxada por picos do sistema operacional; mediana e mínimo ignoram esses picos.
P: Para que serve random.seed(42)?
R: Reprodutibilidade: cada execução sorteia os mesmos alvos e listas; sem isso cada rodada mede um teste diferente.
P: Por que validar a corretude antes do benchmark?
R: Um algoritmo rápido e errado não serve como base de comparação. Compara-se a saída com uma referência (sorted, index) usando assert.
P: Qual a diferença entre contar passos e medir tempo?
R: Passos são propriedade do algoritmo e independem da máquina; tempo depende de CPU, linguagem e sistema, mas captura as constantes que o Big O ignora.
"""
import random
import statistics
import time
import timeit


def bubble_sort(lista):
    lista = list(lista); n = len(lista)
    for p in range(n - 1):
        trocou = False
        for i in range(n - 1 - p):
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]; trocou = True
        if not trocou:
            break
    return lista


if __name__ == "__main__":
    print("1) Resolucao do relogio")
    print(f"   time.time        : {time.get_clock_info('time').resolution:.1e} s")
    print(f"   time.perf_counter: {time.get_clock_info('perf_counter').resolution:.1e} s  <- use este")

    print("\n2) Media x mediana x minimo com um pico do sistema operacional")
    medicoes = [1.01, 0.99, 1.02, 1.00, 0.98, 1.01, 9.50]          # ms; o 9,50 e um pico
    print(f"   medicoes : {medicoes}")
    print(f"   media    : {statistics.mean(medicoes):.2f} ms  (distorcida pelo pico)")
    print(f"   mediana  : {statistics.median(medicoes):.2f} ms  (ignora o pico)")
    print(f"   minimo   : {min(medicoes):.2f} ms  (custo 'limpo')")

    print("\n3) random.seed garante os mesmos sorteios")
    random.seed(42); a = [random.randint(0, 99) for _ in range(6)]
    random.seed(42); b = [random.randint(0, 99) for _ in range(6)]
    print(f"   seed 42 -> {a}\n   seed 42 -> {b}\n   iguais? {a == b}")

    print("\n4) Validar antes de medir")
    random.seed(42)
    for _ in range(200):
        lst = [random.randint(0, 1000) for _ in range(random.randint(0, 30))]
        assert bubble_sort(lst) == sorted(lst), "bubble_sort divergiu de sorted()!"
    print("   bubble_sort conferido contra sorted() em 200 listas aleatorias: OK")

    print("\n5) timeit.repeat: menor tempo de varias rodadas")
    lst = random.sample(range(300), 300)
    tempos = timeit.repeat(lambda: bubble_sort(lst), repeat=5, number=1)
    print(f"   5 rodadas (s): {[round(t, 4) for t in tempos]}")
    print(f"   minimo={min(tempos):.4f} s  mediana={statistics.median(tempos):.4f} s  media={statistics.mean(tempos):.4f} s")
