#!/usr/bin/env python3
"""
ICD-004 - Analise de Algoritmos | Aula 03 - Atividade 01
=========================================================
Comparacao entre Pesquisa Linear (O(n)) e Pesquisa Binaria (O(log n)).

O script prova a diferenca entre os dois algoritmos por duas vias:
  1. Contagem de passos (comparacoes efetivamente executadas);
  2. Benchmark por tempo (time.perf_counter, mediana de varias repeticoes).

Saidas geradas em ./saida:
  - resultados.json  -> dados brutos consumidos por gerar_pdf.py
  - grafico_passos.png / grafico_tempo.png / grafico_speedup.png

Uso:
    python atividade01.py
"""

from __future__ import annotations

import json
import math
import random
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

# ----------------------------------------------------------------------------
# Configuracao
# ----------------------------------------------------------------------------

SEMENTE = 42                                    # reprodutibilidade
TAMANHOS = [1_000, 10_000, 100_000, 1_000_000]  # tamanhos da lista de teste
AMOSTRAS_ALEATORIAS = 25                        # alvos sorteados p/ caso medio
DIR_SAIDA = Path(__file__).parent / "saida"

# Orcamento de tempo por medicao (s). O numero de repeticoes se adapta ao custo
# do algoritmo: a binaria e tao rapida que precisa de muitas repeticoes para
# sair do ruido do relogio; a linear em 1e6 itens precisa de poucas.
ORCAMENTO_S = 0.20
REPETICOES_MIN = 3
REPETICOES_MAX = 2_000

CENARIOS = [
    "melhor caso (1o elemento)",
    "pior caso (ultimo elemento)",
    "pior caso (alvo ausente)",
    "caso medio (aleatorio)",
]


# ----------------------------------------------------------------------------
# 1. Os dois algoritmos de busca
# ----------------------------------------------------------------------------

def busca_linear(lista: list[int], alvo: int) -> tuple[int, int]:
    """Pesquisa linear - O(n).

    Percorre a lista do inicio ao fim comparando elemento por elemento.
    Nao exige lista ordenada.

    Retorna (indice, passos); indice == -1 quando o alvo nao existe.
    """
    passos = 0
    for indice, valor in enumerate(lista):
        passos += 1                  # 1 passo = 1 comparacao
        if valor == alvo:
            return indice, passos
    return -1, passos


def busca_binaria(lista: list[int], alvo: int) -> tuple[int, int]:
    """Pesquisa binaria - O(log n).

    A cada passo descarta metade do espaco de busca. EXIGE lista ordenada,
    pois usa a comparacao com o elemento do meio para decidir qual metade
    ainda pode conter o alvo.

    Retorna (indice, passos); indice == -1 quando o alvo nao existe.
    """
    passos = 0
    baixo, alto = 0, len(lista) - 1
    while baixo <= alto:
        passos += 1                  # 1 passo = 1 comparacao com o meio
        meio = (baixo + alto) // 2
        chute = lista[meio]
        if chute == alvo:
            return meio, passos
        if chute < alvo:
            baixo = meio + 1         # descarta a metade da esquerda
        else:
            alto = meio - 1          # descarta a metade da direita
    return -1, passos


# ----------------------------------------------------------------------------
# 2. Instrumentacao: passos e tempo
# ----------------------------------------------------------------------------

@dataclass
class Medicao:
    """Resultado de um cenario (algoritmo + tipo de alvo) para um tamanho n."""
    algoritmo: str
    cenario: str
    n: int
    passos: float
    tempo_us: float          # mediana em microssegundos
    repeticoes: int
    indice: int


def cronometrar(funcao, lista: list[int], alvo: int) -> tuple[float, int]:
    """Mede o tempo de funcao(lista, alvo); devolve (mediana_us, repeticoes).

    Repete a chamada ate estourar ORCAMENTO_S (respeitando os limites min/max)
    e usa a MEDIANA das amostras, mais robusta a interferencia do sistema
    operacional do que a media.
    """
    amostras: list[float] = []
    inicio_total = time.perf_counter()
    while True:
        t0 = time.perf_counter()
        funcao(lista, alvo)
        amostras.append((time.perf_counter() - t0) * 1_000_000)   # s -> us
        if len(amostras) >= REPETICOES_MAX:
            break
        if (len(amostras) >= REPETICOES_MIN
                and (time.perf_counter() - inicio_total) > ORCAMENTO_S):
            break
    return statistics.median(amostras), len(amostras)


def medir_cenario(nome_alg, funcao, lista, alvo, cenario) -> Medicao:
    indice, passos = funcao(lista, alvo)
    tempo_us, repeticoes = cronometrar(funcao, lista, alvo)
    return Medicao(nome_alg, cenario, len(lista), float(passos),
                   tempo_us, repeticoes, indice)


def medir_caso_medio(nome_alg, funcao, lista, alvos, cenario) -> Medicao:
    """Caso medio: media dos passos e mediana dos tempos sobre varios alvos."""
    passos: list[int] = []
    tempos: list[float] = []
    repeticoes = 0
    for alvo in alvos:
        _, p = funcao(lista, alvo)
        t, r = cronometrar(funcao, lista, alvo)
        passos.append(p)
        tempos.append(t)
        repeticoes += r
    return Medicao(nome_alg, cenario, len(lista), statistics.mean(passos),
                   statistics.median(tempos), repeticoes, -2)


# ----------------------------------------------------------------------------
# 3. Execucao do experimento
# ----------------------------------------------------------------------------

def validar_algoritmos() -> list[str]:
    """Testes de sanidade: os dois algoritmos precisam concordar sempre."""
    random.seed(SEMENTE)
    log: list[str] = []
    lista = list(range(0, 2_000, 2))            # pares de 0 a 1998 (ordenada)

    for alvo in (0, 998, 1998, -1, 999, 2_000):  # existentes e inexistentes
        i_lin, _ = busca_linear(lista, alvo)
        i_bin, _ = busca_binaria(lista, alvo)
        assert i_lin == i_bin, f"divergencia no alvo {alvo}: {i_lin} != {i_bin}"
    log.append(f"OK: 6 alvos-chave conferidos em lista de {len(lista)} itens.")

    for _ in range(500):                        # fuzzing
        alvo = random.randint(-10, 2_010)
        assert busca_linear(lista, alvo)[0] == busca_binaria(lista, alvo)[0]
    log.append("OK: 500 alvos aleatorios - linear e binaria retornaram o mesmo "
               "indice em todos.")

    # Limite teorico: a binaria nunca deve passar de floor(log2(n)) + 1 passos.
    for n in (1, 2, 3, 7, 8, 1_000, 100_000):
        l = list(range(n))
        pior = max(busca_binaria(l, -1)[1], busca_binaria(l, n)[1])
        limite = math.floor(math.log2(n)) + 1
        assert pior <= limite, f"n={n}: {pior} passos > limite {limite}"
    log.append("OK: passos da binaria <= floor(log2(n))+1 em todos os n "
               "testados (limite teorico respeitado).")

    assert busca_linear([], 1) == (-1, 0) and busca_binaria([], 1) == (-1, 0)
    assert busca_linear([5], 5)[0] == 0 and busca_binaria([5], 5)[0] == 0
    log.append("OK: casos de borda (lista vazia e lista unitaria).")
    return log


def executar() -> dict:
    random.seed(SEMENTE)
    medicoes: list[Medicao] = []

    print("=" * 76)
    print("ATIVIDADE 01 - PESQUISA LINEAR (O(n)) vs PESQUISA BINARIA (O(log n))")
    print("=" * 76)

    log_validacao = validar_algoritmos()
    print("\n[1] VALIDACAO DE CORRETUDE")
    for linha in log_validacao:
        print("    " + linha)

    print("\n[2] EXPERIMENTO (mediana de varias repeticoes por medicao)")
    for n in TAMANHOS:
        # Lista grande, ordenada e sem repeticoes: pre-requisito da binaria.
        lista = list(range(n))
        alvos = [random.randrange(n) for _ in range(AMOSTRAS_ALEATORIAS)]

        for cenario, alvo in (("melhor caso (1o elemento)", 0),
                              ("pior caso (ultimo elemento)", n - 1),
                              ("pior caso (alvo ausente)", -1)):
            medicoes.append(medir_cenario("linear", busca_linear, lista, alvo, cenario))
            medicoes.append(medir_cenario("binaria", busca_binaria, lista, alvo, cenario))

        medicoes.append(medir_caso_medio("linear", busca_linear, lista, alvos,
                                        "caso medio (aleatorio)"))
        medicoes.append(medir_caso_medio("binaria", busca_binaria, lista, alvos,
                                         "caso medio (aleatorio)"))
        print(f"    n = {fmt(n):>11} ... concluido")

    return {
        "config": {
            "semente": SEMENTE,
            "tamanhos": TAMANHOS,
            "amostras_aleatorias": AMOSTRAS_ALEATORIAS,
            "orcamento_s": ORCAMENTO_S,
            "python": sys.version.split()[0],
        },
        "validacao": log_validacao,
        "medicoes": [asdict(m) for m in medicoes],
    }


# ----------------------------------------------------------------------------
# 4. Relatorio em texto
# ----------------------------------------------------------------------------

def fmt(valor: float, casas: int = 0) -> str:
    """Formata numero no padrao brasileiro: 1.000.000,00"""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")


def fmt_razao(valor: float) -> str:
    """Razoes pequenas (< 10) precisam de decimais para nao virarem '0x'."""
    return fmt(valor, 2 if valor < 10 else 0) + "x"


def buscar(medicoes: list[dict], algoritmo: str, cenario: str, n: int) -> dict:
    for m in medicoes:
        if m["algoritmo"] == algoritmo and m["cenario"] == cenario and m["n"] == n:
            return m
    raise KeyError((algoritmo, cenario, n))


def imprimir_tabelas(dados: dict) -> None:
    med = dados["medicoes"]
    tamanhos = dados["config"]["tamanhos"]

    print("\n[3] PASSOS (comparacoes executadas)")
    print(f"    {'cenario':<30}{'n':>11}{'linear':>12}{'binaria':>10}{'razao':>12}")
    print("    " + "-" * 75)
    for cenario in CENARIOS:
        for n in tamanhos:
            l = buscar(med, "linear", cenario, n)["passos"]
            b = buscar(med, "binaria", cenario, n)["passos"]
            print(f"    {cenario:<30}{fmt(n):>11}{fmt(l, 1):>12}"
                  f"{fmt(b, 1):>10}{fmt_razao(l / b):>12}")
        print()

    print("[4] TEMPO (mediana, microssegundos)")
    print(f"    {'cenario':<30}{'n':>11}{'linear':>14}{'binaria':>12}{'speedup':>12}")
    print("    " + "-" * 79)
    for cenario in CENARIOS:
        for n in tamanhos:
            l = buscar(med, "linear", cenario, n)["tempo_us"]
            b = buscar(med, "binaria", cenario, n)["tempo_us"]
            print(f"    {cenario:<30}{fmt(n):>11}{fmt(l, 2):>14}"
                  f"{fmt(b, 2):>12}{fmt_razao(l / b):>12}")
        print()

    n_max = tamanhos[-1]
    pior = "pior caso (alvo ausente)"
    p_lin = buscar(med, "linear", pior, n_max)["passos"]
    p_bin = buscar(med, "binaria", pior, n_max)["passos"]
    t_lin = buscar(med, "linear", pior, n_max)["tempo_us"]
    t_bin = buscar(med, "binaria", pior, n_max)["tempo_us"]
    print(f"[5] CONCLUSAO NUMERICA (pior caso, n = {fmt(n_max)})")
    print(f"    Passos : linear {fmt(p_lin)} x binaria {fmt(p_bin)}"
          f"  ->  {fmt(p_lin / p_bin)}x menos passos")
    print(f"    Tempo  : linear {fmt(t_lin, 2)} us x binaria {fmt(t_bin, 2)} us"
          f"  ->  {fmt(t_lin / t_bin)}x mais rapida")
    print(f"    log2({fmt(n_max)}) = {fmt(math.log2(n_max), 2)}  "
          f"(limite teorico da binaria: {math.floor(math.log2(n_max)) + 1} passos)")


# ----------------------------------------------------------------------------
# 5. Custo da ordenacao e ponto de equilibrio
# ----------------------------------------------------------------------------

def experimento_ordenacao(dados: dict) -> dict:
    """Mede o preco do pre-requisito da binaria: ordenar a lista.

    Ordenar custa O(n log n) - MAIS que uma unica busca linear O(n). Logo a
    binaria so compensa se a lista ja estiver ordenada ou se o custo da
    ordenacao for amortizado por muitas consultas. O ponto de equilibrio k e o
    numero de consultas a partir do qual "ordenar + k buscas binarias" fica
    mais barato que "k buscas lineares":

        k * t_lin  >  t_ord + k * t_bin   =>   k > t_ord / (t_lin - t_bin)
    """
    n = dados["config"]["tamanhos"][-1]
    random.seed(SEMENTE)
    base = list(range(n))
    random.shuffle(base)

    amostras: list[float] = []
    for _ in range(5):
        copia = list(base)                       # copia fora da medicao
        t0 = time.perf_counter()
        copia.sort()                             # Timsort - O(n log n)
        amostras.append((time.perf_counter() - t0) * 1_000_000)
    t_ord = statistics.median(amostras)

    cen = "caso medio (aleatorio)"
    t_lin = buscar(dados["medicoes"], "linear", cen, n)["tempo_us"]
    t_bin = buscar(dados["medicoes"], "binaria", cen, n)["tempo_us"]
    k = t_ord / (t_lin - t_bin)

    print(f"\n[6] CUSTO DA ORDENACAO (n = {fmt(n)})")
    print(f"    Ordenar a lista (list.sort, O(n log n)) : {fmt(t_ord, 2)} us")
    print(f"    1 busca linear (caso medio)             : {fmt(t_lin, 2)} us")
    print(f"    1 busca binaria (caso medio)            : {fmt(t_bin, 2)} us")
    print(f"    Ponto de equilibrio                     : {fmt(k, 1)} consultas")
    print(f"    -> Abaixo de ~{math.ceil(k)} consultas, vale mais a pena a busca")
    print("       linear na lista desordenada; acima disso, ordenar uma vez e")
    print("       usar a binaria em todas as consultas seguintes.")

    return {"n": n, "tempo_ordenacao_us": t_ord, "tempo_linear_us": t_lin,
            "tempo_binaria_us": t_bin, "equilibrio_consultas": k}


# ----------------------------------------------------------------------------
# 6. Graficos
# ----------------------------------------------------------------------------

def gerar_graficos(dados: dict) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ns = dados["config"]["tamanhos"]
    med = dados["medicoes"]
    cen_pior, cen_medio = "pior caso (alvo ausente)", "caso medio (aleatorio)"
    COR_LIN, COR_BIN, COR_REF = "#c0392b", "#1f6feb", "#7d8590"
    arquivos: list[Path] = []

    # (a) Passos no pior caso -------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=160)
    p_lin = [buscar(med, "linear", cen_pior, n)["passos"] for n in ns]
    p_bin = [buscar(med, "binaria", cen_pior, n)["passos"] for n in ns]
    ax.plot(ns, p_lin, "o-", color=COR_LIN, label="Linear — O(n)")
    ax.plot(ns, p_bin, "s-", color=COR_BIN, label="Binária — O(log n)")
    ax.plot(ns, [math.floor(math.log2(n)) + 1 for n in ns], "--",
            color=COR_REF, label="limite teórico log₂(n)+1")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamanho da lista (n)")
    ax.set_ylabel("Passos (escala log)")
    ax.set_title("Passos no pior caso: crescimento linear vs logarítmico")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    ax.set_ylim(bottom=4)          # espaco para os rotulos abaixo dos pontos
    for x, y in zip(ns, p_bin):
        ax.annotate(f"{y:.0f}", (x, y), textcoords="offset points",
                    xytext=(0, -15), ha="center", fontsize=8, color=COR_BIN)
    fig.tight_layout()
    caminho = DIR_SAIDA / "grafico_passos.png"
    fig.savefig(caminho)
    plt.close(fig)
    arquivos.append(caminho)

    # (b) Benchmark por tempo -------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=160)
    for cen, estilo in ((cen_pior, "-"), (cen_medio, ":")):
        rot = "pior caso" if cen == cen_pior else "caso médio"
        ax.plot(ns, [buscar(med, "linear", cen, n)["tempo_us"] for n in ns],
                "o" + estilo, color=COR_LIN, label=f"Linear ({rot})")
        ax.plot(ns, [buscar(med, "binaria", cen, n)["tempo_us"] for n in ns],
                "s" + estilo, color=COR_BIN, label=f"Binária ({rot})")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamanho da lista (n)")
    ax.set_ylabel("Tempo mediano (µs, escala log)")
    ax.set_title("Benchmark por tempo")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    caminho = DIR_SAIDA / "grafico_tempo.png"
    fig.savefig(caminho)
    plt.close(fig)
    arquivos.append(caminho)

    # (c) Speedup -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=160)
    speedup = [buscar(med, "linear", cen_pior, n)["tempo_us"]
               / buscar(med, "binaria", cen_pior, n)["tempo_us"] for n in ns]
    barras = ax.bar([fmt(n) for n in ns], speedup, color="#2f81f7", width=0.55)
    ax.bar_label(barras, fmt="%.0fx", padding=3, fontsize=9)
    ax.set_xlabel("Tamanho da lista (n)")
    ax.set_ylabel("Quantas vezes mais rápida")
    ax.set_title("Ganho de tempo da binária sobre a linear (pior caso)")
    ax.margins(y=0.18)
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    caminho = DIR_SAIDA / "grafico_speedup.png"
    fig.savefig(caminho)
    plt.close(fig)
    arquivos.append(caminho)

    return arquivos


# ----------------------------------------------------------------------------
def main() -> None:
    DIR_SAIDA.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    dados = executar()
    imprimir_tabelas(dados)
    dados["ordenacao"] = experimento_ordenacao(dados)

    dados["graficos"] = [p.name for p in gerar_graficos(dados)]
    dados["duracao_total_s"] = round(time.perf_counter() - t0, 2)

    destino = DIR_SAIDA / "resultados.json"
    destino.write_text(json.dumps(dados, indent=2, ensure_ascii=False),
                       encoding="utf-8")

    print(f"\n[7] ARQUIVOS GERADOS ({fmt(dados['duracao_total_s'], 2)} s de execucao)")
    print(f"    {destino}")
    for grafico in dados["graficos"]:
        print(f"    {DIR_SAIDA / grafico}")


if __name__ == "__main__":
    main()
