"""
ICD-004 - Analise de Algoritmos
Aula 04 - Atividade 02

Implementa o BUBBLE SORT contando COMPARACOES e TROCAS, testa os tres
cenarios (melhor, medio e pior caso) e compara com o SELECTION SORT.

Para rodar:  python bubble_sort.py
"""

import random
from pathlib import Path

# Pasta onde este arquivo esta (para salvar os resultados aqui do lado).
PASTA = Path(__file__).parent

# ---------------------------------------------------------------------------
# Configuracao do teste
# ---------------------------------------------------------------------------
# Listas de exemplo do enunciado (n = 5)
MELHOR_CASO = [1, 2, 3, 4, 5]      # ja ordenada
MEDIO_CASO = [3, 5, 1, 4, 2]       # ordem aleatoria
PIOR_CASO = [5, 4, 3, 2, 1]        # ordem inversa

EXEMPLO_ENUNCIADO = [6, 3, 8, 5, 2]

TAMANHOS = [5, 10, 50, 100, 500]   # para mostrar o crescimento das operacoes
SEMENTE = 42                       # deixa o sorteio sempre igual


# ---------------------------------------------------------------------------
# 1) BUBBLE SORT - O(n^2)
#    Compara pares VIZINHOS e troca quando estao fora de ordem.
#    A cada passagem o maior elemento "sobe" para o final da lista.
#    Se uma passagem inteira nao trocar nada, a lista ja esta ordenada e o
#    algoritmo para - foi o que o enunciado pediu: "repete as passagens ate
#    nao haver mais trocas".
# ---------------------------------------------------------------------------
def bubble_sort(lista_original):
    lista = list(lista_original)        # copia, para nao alterar a original
    comparacoes = 0
    trocas = 0
    n = len(lista)

    for passagem in range(n - 1):
        houve_troca = False

        # A cada passagem o fim da lista ja esta ordenado, entao olhamos um
        # elemento a menos: por isso o "- passagem".
        for i in range(n - 1 - passagem):
            comparacoes += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                trocas += 1
                houve_troca = True

        if not houve_troca:             # passagem sem nenhuma troca -> ordenada
            break

    return lista, comparacoes, trocas


# ---------------------------------------------------------------------------
# 2) SELECTION SORT - O(n^2)
#    Procura o MENOR elemento do trecho que ainda falta ordenar e o coloca na
#    posicao correta. Faz muitas comparacoes, mas pouquissimas trocas.
# ---------------------------------------------------------------------------
def selection_sort(lista_original):
    lista = list(lista_original)
    comparacoes = 0
    trocas = 0
    n = len(lista)

    for inicio in range(n - 1):
        menor = inicio                  # supoe que o primeiro e o menor

        for i in range(inicio + 1, n):
            comparacoes += 1
            if lista[i] < lista[menor]:
                menor = i               # achou um elemento menor ainda

        if menor != inicio:             # so troca se o menor mudou de lugar
            lista[inicio], lista[menor] = lista[menor], lista[inicio]
            trocas += 1

    return lista, comparacoes, trocas


# ---------------------------------------------------------------------------
# 3) Programa principal
# ---------------------------------------------------------------------------

# Tudo o que for mostrado na tela tambem fica guardado aqui, para o PDF.
relatorio = []


def mostrar(texto=""):
    print(texto)
    relatorio.append(texto)


def bubble_sort_passo_a_passo(lista_original):
    """Mesmo algoritmo do item 1, mas mostrando cada comparacao (didatico)."""
    lista = list(lista_original)
    comparacoes = 0
    trocas = 0
    n = len(lista)
    nomes = ["Primeira", "Segunda", "Terceira", "Quarta", "Quinta"]

    for passagem in range(n - 1):
        mostrar(f"  {nomes[passagem]} passagem:")
        houve_troca = False

        for i in range(n - 1 - passagem):
            a = lista[i]
            b = lista[i + 1]
            comparacoes += 1
            if a > b:
                lista[i], lista[i + 1] = b, a
                trocas += 1
                houve_troca = True
                acao = "troca    "
            else:
                acao = "nao troca"
            mostrar(f"    compara {a} e {b} -> {acao} -> {lista}")

        if not houve_troca:
            mostrar("    nenhuma troca nesta passagem -> lista ordenada")
            break
        mostrar()

    return lista, comparacoes, trocas


mostrar("BUBBLE SORT: CONTAGEM DE OPERACOES E COMPARACAO COM O SELECTION SORT")
mostrar("=" * 70)
mostrar()


# --- Parte 1: passo a passo do exemplo do enunciado -------------------------
mostrar(f"1) PASSO A PASSO DO EXEMPLO DO ENUNCIADO {EXEMPLO_ENUNCIADO}")
mostrar("-" * 70)
_final, _comp, _troc = bubble_sort_passo_a_passo(EXEMPLO_ENUNCIADO)
mostrar(f"  resultado final: {_final} ({_comp} comparacoes, {_troc} trocas)")
mostrar()


# --- Parte 2: os tres cenarios pedidos (n = 5) ------------------------------
cenarios = [
    ("Melhor caso (ja ordenada)", MELHOR_CASO),
    ("Medio caso (aleatoria)", MEDIO_CASO),
    ("Pior caso (invertida)", PIOR_CASO),
]

mostrar("2) OS TRES CENARIOS COM n = 5")
mostrar("-" * 70)
mostrar(f"  {'Cenario':<26} {'Lista':<17} "
        f"{'BUBBLE SORT':<16} {'SELECTION SORT':<16}")
mostrar(f"  {'':<26} {'':<17} "
        f"{'comp / trocas':<16} {'comp / trocas':<16}")

linhas_cenarios = ["cenario,lista,bubble_comparacoes,bubble_trocas,"
                   "selection_comparacoes,selection_trocas"]

for nome, lista in cenarios:
    saida_bubble, comp_b, troc_b = bubble_sort(lista)
    saida_selection, comp_s, troc_s = selection_sort(lista)

    # Confere se as duas ordenacoes chegaram ao mesmo resultado correto.
    assert saida_bubble == saida_selection == sorted(lista)

    mostrar(f"  {nome:<26} {str(lista):<17} "
            f"{comp_b:>4} / {troc_b:<9} {comp_s:>4} / {troc_s:<9}")
    linhas_cenarios.append(f'{nome},"{lista}",{comp_b},{troc_b},'
                           f'{comp_s},{troc_s}')
mostrar()

# --- Parte 3: como as operacoes crescem quando a lista aumenta --------------
mostrar("3) CRESCIMENTO DAS OPERACOES CONFORME O TAMANHO DA LISTA")
mostrar("-" * 70)
mostrar(f"  {'n':>4}  {'cenario':<8} "
        f"{'bubble comp':>12} {'bubble trocas':>14} "
        f"{'select comp':>12} {'select trocas':>14}")

random.seed(SEMENTE)                    # sorteio sempre igual -> resultado igual
linhas_csv = ["n,cenario,bubble_comparacoes,bubble_trocas,"
              "selection_comparacoes,selection_trocas"]

for n in TAMANHOS:
    listas_do_tamanho = [
        ("melhor", list(range(1, n + 1))),                  # ja ordenada
        ("medio", random.sample(range(1, n + 1), n)),       # embaralhada
        ("pior", list(range(n, 0, -1))),                    # invertida
    ]

    for rotulo, lista in listas_do_tamanho:
        _, comp_b, troc_b = bubble_sort(lista)
        _, comp_s, troc_s = selection_sort(lista)
        mostrar(f"  {n:>4}  {rotulo:<8} "
                f"{comp_b:>12} {troc_b:>14} {comp_s:>12} {troc_s:>14}")
        linhas_csv.append(f"{n},{rotulo},{comp_b},{troc_b},{comp_s},{troc_s}")
    mostrar()

# --- Partes 4 e 5: analise dos resultados -----------------------------------
tamanho = len(MELHOR_CASO)
maximo = tamanho * (tamanho - 1) // 2   # n(n-1)/2 = numero maximo de comparacoes

mostrar("4) POR QUE O NUMERO DE OPERACOES VARIA?")
mostrar("-" * 70)
mostrar("  O Bubble Sort so troca quando encontra um par vizinho fora de")
mostrar("  ordem. Logo, o trabalho dele depende de QUANTO a lista ja esta")
mostrar("  ordenada:")
mostrar()
mostrar("  - Melhor caso (lista ordenada): a primeira passagem nao troca")
mostrar("    nada, o algoritmo percebe isso e para. Faz apenas n-1 =")
mostrar(f"    {tamanho - 1} comparacoes e 0 trocas. Comportamento O(n).")
mostrar()
mostrar("  - Pior caso (lista invertida): TODO par comparado esta fora de")
mostrar("    ordem, entao ele troca em todas as comparacoes. Faz")
mostrar(f"    n(n-1)/2 = {maximo} comparacoes e {maximo} trocas. Comportamento O(n^2).")
mostrar()
mostrar("  - Medio caso (lista aleatoria): fica entre os dois. Em media")
mostrar("    metade dos pares esta fora de ordem, entao o numero de trocas")
mostrar("    fica perto da metade do pior caso. Tambem e O(n^2).")
mostrar()
mostrar("  A tabela do item 3 confirma: quando n dobra, as comparacoes do")
mostrar("  pior caso ficam cerca de 4 vezes maiores - exatamente o que se")
mostrar("  espera de um algoritmo quadratico (2^2 = 4).")
mostrar()

mostrar("5) COMPARACAO COM O SELECTION SORT")
mostrar("-" * 70)
mostrar("  O Selection Sort percorre todo o trecho restante para achar o")
mostrar("  menor elemento, sem aproveitar a ordem que ja existe. Por isso")
mostrar("  ele faz SEMPRE n(n-1)/2 comparacoes, nos tres cenarios: com")
mostrar(f"  n = 5 sao {maximo} comparacoes na lista ordenada, na aleatoria e na")
mostrar("  invertida. Ele e O(n^2) inclusive no melhor caso.")
mostrar()
mostrar("  Em compensacao, faz no maximo n-1 trocas, porque cada elemento")
mostrar(f"  vai direto para o lugar certo. O Bubble Sort chega a {maximo} trocas")
mostrar(f"  com n = {tamanho}.")
mostrar()
mostrar("  Resumindo:")
mostrar("  - lista quase ordenada -> Bubble Sort vence (para cedo, O(n)).")
mostrar("  - trocas caras (registros grandes) -> Selection Sort vence,")
mostrar("    porque movimenta muito menos dados.")
mostrar("  - listas grandes -> os dois sao ruins, O(n^2). Vale usar")
mostrar("    algoritmos O(n log n), como Merge Sort ou Quick Sort.")

# ---------------------------------------------------------------------------
# 4) Salva os resultados em arquivos, para montar o PDF depois
# ---------------------------------------------------------------------------
(PASTA / "resultado.txt").write_text("\n".join(relatorio), encoding="utf-8")
(PASTA / "operacoes.csv").write_text("\n".join(linhas_csv), encoding="utf-8")
(PASTA / "cenarios.csv").write_text("\n".join(linhas_cenarios), encoding="utf-8")

print()
print("Resultados salvos em: resultado.txt, operacoes.csv e cenarios.csv")
