"""
ICD-004 - Analise de Algoritmos
Aula 03 - Atividade 01

Compara a BUSCA LINEAR (O(n)) com a BUSCA BINARIA (O(log n)),
medindo o TEMPO que cada uma leva em varias execucoes.

Para rodar:  python busca_linear_vs_binaria.py
"""

import time
from pathlib import Path

# Pasta onde este arquivo esta (para salvar os resultados aqui do lado).
PASTA = Path(__file__).parent

# ---------------------------------------------------------------------------
# Configuracao do teste
# ---------------------------------------------------------------------------
TAMANHO = 1000000     # lista grande: 1 milhao de numeros
EXECUCOES = 3         # quantas vezes vamos repetir o teste


# ---------------------------------------------------------------------------
# 1) BUSCA LINEAR - O(n)
#    Olha um elemento por vez, do inicio ao fim, ate achar.
#    Nao precisa de lista ordenada.
# ---------------------------------------------------------------------------
def busca_linear(lista, alvo):
    passos = 0
    for posicao in range(len(lista)):
        passos = passos + 1                 # contou mais uma comparacao
        if lista[posicao] == alvo:
            return posicao, passos          # achou!
    return -1, passos                       # nao achou


# ---------------------------------------------------------------------------
# 2) BUSCA BINARIA - O(log n)
#    Olha o elemento do MEIO e joga fora a metade que nao pode conter o alvo.
#    So funciona se a lista estiver ORDENADA.
# ---------------------------------------------------------------------------
def busca_binaria(lista, alvo):
    passos = 0
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        passos = passos + 1                 # contou mais uma comparacao
        meio = (inicio + fim) // 2

        if lista[meio] == alvo:
            return meio, passos             # achou!
        if lista[meio] < alvo:
            inicio = meio + 1               # o alvo esta na metade da DIREITA
        else:
            fim = meio - 1                  # o alvo esta na metade da ESQUERDA

    return -1, passos                       # nao achou


# ---------------------------------------------------------------------------
# 3) Mede o tempo de uma busca
#    time.perf_counter() devolve o "cronometro" do computador em segundos.
# ---------------------------------------------------------------------------
def medir_tempo(funcao_de_busca, lista, alvo):
    comeco = time.perf_counter()
    posicao, passos = funcao_de_busca(lista, alvo)
    fim = time.perf_counter()

    tempo_ms = (fim - comeco) * 1000        # segundos -> milissegundos
    return posicao, passos, tempo_ms


# ---------------------------------------------------------------------------
# 4) Programa principal
# ---------------------------------------------------------------------------

# Tudo o que for mostrado na tela tambem fica guardado aqui, para o PDF.
relatorio = []


def mostrar(texto=""):
    print(texto)
    relatorio.append(texto)


# A lista precisa estar ordenada por causa da busca binaria.
lista = list(range(TAMANHO))     # 0, 1, 2, 3, ... 999999
alvo = TAMANHO - 1               # o ULTIMO numero = pior caso para a linear

mostrar("COMPARACAO POR TEMPO: BUSCA LINEAR x BUSCA BINARIA")
mostrar("=" * 66)
mostrar(f"Tamanho da lista ..: {TAMANHO} numeros (de 0 ate {TAMANHO - 1})")
mostrar(f"Numero procurado ..: {alvo} (o ultimo da lista = pior caso)")
mostrar(f"Execucoes .........: {EXECUCOES}")
mostrar()

tempos_linear = []
tempos_binaria = []

for execucao in range(1, EXECUCOES + 1):
    mostrar(f"EXECUCAO {execucao}")

    # 1o resultado: busca linear
    posicao1, passos1, tempo1 = medir_tempo(busca_linear, lista, alvo)
    mostrar(f"  1o resultado - busca linear  : posicao {posicao1} | "
            f"{passos1:>7} passos | {tempo1:>9.4f} ms")

    # 2o resultado: busca binaria
    posicao2, passos2, tempo2 = medir_tempo(busca_binaria, lista, alvo)
    mostrar(f"  2o resultado - busca binaria : posicao {posicao2} | "
            f"{passos2:>7} passos | {tempo2:>9.4f} ms")

    mostrar(f"  --> a binaria foi {tempo1 / tempo2:.0f} vezes mais rapida")
    mostrar()

    tempos_linear.append(tempo1)
    tempos_binaria.append(tempo2)

# Media dos tempos das execucoes
media_linear = sum(tempos_linear) / EXECUCOES
media_binaria = sum(tempos_binaria) / EXECUCOES

mostrar(f"MEDIA DAS {EXECUCOES} EXECUCOES")
mostrar("=" * 66)
mostrar(f"  Busca linear  - O(n) .....: {media_linear:>9.4f} ms")
mostrar(f"  Busca binaria - O(log n) .: {media_binaria:>9.4f} ms")
mostrar(f"  A busca binaria foi {media_linear / media_binaria:.0f} vezes mais rapida.")
mostrar()
mostrar("PASSOS NO PIOR CASO (o que explica a diferenca de tempo)")
mostrar("=" * 66)
mostrar(f"  Busca linear  : {passos1} passos (olhou a lista toda)")
mostrar(f"  Busca binaria : {passos2} passos (cortou a lista no meio {passos2} vezes)")

# ---------------------------------------------------------------------------
# 5) Salva os resultados em arquivos, para o gerar_pdf.py usar
# ---------------------------------------------------------------------------
(PASTA / "resultado.txt").write_text("\n".join(relatorio), encoding="utf-8")

linhas_csv = ["execucao,tempo_linear_ms,tempo_binaria_ms"]
for i in range(EXECUCOES):
    linhas_csv.append(f"{i + 1},{tempos_linear[i]:.4f},{tempos_binaria[i]:.4f}")
(PASTA / "tempos.csv").write_text("\n".join(linhas_csv), encoding="utf-8")

print()
print("Resultados salvos em: resultado.txt e tempos.csv")
