"""[04] Benchmark: busca linear x busca binária (passos e tempo) — repete a Atividade 01
Tema: Busca / Medição | Complexidade: O(n) x O(log n) | Memória: O(1)
Palavras-chave: benchmark, tempo, perf_counter, mediana, passos x tempo, busca linear, busca binária, pior caso, 1 milhão, atividade 01, speedup

O que faz:
- Cria uma lista de 1.000.000 de números e procura o último (pior caso) com os dois algoritmos.
- Conta passos e mede tempo com perf_counter, repetindo 5 vezes e usando a MEDIANA.
- Mostra a razão de passos (50.000x) e a razão de tempo (bem menor), e explica a diferença.

Perguntas prováveis:
P: Por que medir passos E tempo?
R: Passos são propriedade do algoritmo (iguais em qualquer máquina) e provam a classe Big O; tempo é o que o usuário sente e inclui as constantes que o Big O ignora. Quando os dois concordam, a conclusão é robusta.
P: Por que a razão de tempo é menor que a razão de passos?
R: Passos não são segundos: cada passo da binária faz mais operações (divisão, comparação, dois índices) que o passo da linear, e há custos fixos de chamada e de resolução do relógio.
P: Por que usar mediana em vez de média?
R: A média é puxada por picos do sistema operacional (outros processos); a mediana ignora esses picos e reflete o custo típico.
P: Por que usar uma lista grande?
R: Com n pequeno, a diferença entre O(n) e O(log n) se perde nas constantes e no ruído do relógio.
"""
import statistics
import time


def busca_linear(lista, alvo):
    passos = 0
    for i in range(len(lista)):
        passos += 1
        if lista[i] == alvo:
            return i, passos
    return None, passos


def busca_binaria(lista, alvo):
    baixo, alto, passos = 0, len(lista) - 1, 0
    while baixo <= alto:
        passos += 1
        meio = (baixo + alto) // 2
        if lista[meio] == alvo:
            return meio, passos
        if lista[meio] < alvo:
            baixo = meio + 1
        else:
            alto = meio - 1
    return None, passos


def cronometrar(funcao, lista, alvo, repeticoes=5):
    """Mediana do tempo (ms) de `repeticoes` execucoes."""
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao(lista, alvo)
        tempos.append((time.perf_counter() - inicio) * 1000)
    return statistics.median(tempos)


if __name__ == "__main__":
    n = 1_000_000
    lista = list(range(n))
    alvo = n - 1                                   # ultimo elemento = pior caso

    _, passos_lin = busca_linear(lista, alvo)
    _, passos_bin = busca_binaria(lista, alvo)
    t_lin = cronometrar(busca_linear, lista, alvo)
    t_bin = cronometrar(busca_binaria, lista, alvo, repeticoes=50)

    print(f"Lista de {n:_} elementos, alvo = ultimo (pior caso)".replace("_", "."))
    print("-" * 60)
    print(f"Busca linear  - O(n)     : {passos_lin:>9} passos | {t_lin:>10.4f} ms")
    print(f"Busca binaria - O(log n) : {passos_bin:>9} passos | {t_bin:>10.4f} ms")
    print(f"\nRazao de passos: {passos_lin / passos_bin:>10.0f} x")
    print(f"Razao de tempo : {t_lin / t_bin:>10.0f} x")
    print("\nA razao de tempo e menor porque cada passo da binaria custa mais que um")
    print("passo da linear e ha custos fixos (chamada, relogio). Passos nao sao segundos.")
