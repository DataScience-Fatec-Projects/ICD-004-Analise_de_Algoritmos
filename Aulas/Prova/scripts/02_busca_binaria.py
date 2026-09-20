"""[02] Busca binária iterativa com rastreamento de baixo/alto/meio
Tema: Busca | Complexidade: melhor O(1), médio e pior O(log n) | Memória: O(1)
Palavras-chave: busca binária, lista ordenada, meio, metade, log2, baixo, alto, chute, descartar metade, passos, 128, 1 milhão

O que faz:
- Faz a busca binária em uma lista ORDENADA mostrando, a cada passo, o intervalo [baixo, alto], o meio e a decisão tomada.
- Mostra um alvo presente, um no início e um ausente.
- Compara os passos medidos no pior caso com floor(log2 n) + 1 e com o teto do livro, log2 n arredondado para cima.

Perguntas prováveis:
P: Por que a lista precisa estar ordenada?
R: Porque a cada passo o algoritmo descarta uma metade inteira com base na comparação com o elemento do meio; isso só vale se tudo à esquerda for menor e tudo à direita for maior.
P: Quantos passos no máximo para n = 128? E para n = 1.000.000? (Livro, ex. 1.1)
R: log2 128 = 7 passos pela conta do livro (uma implementação que conta a comparação final chega a 8). Para 1.000.000: 20 passos, pois 2^20 = 1.048.576.
P: O que acontece quando o alvo não está na lista?
R: O intervalo encolhe até baixo ficar maior que alto; o laço termina e devolve None, ainda em O(log n) passos.
P: Qual é o melhor caso da busca binária?
R: O alvo está exatamente no meio da lista: 1 passo, O(1).
P: Se a lista dobra de tamanho, quantos passos a mais? (Livro, ex. 1.2)
R: Apenas 1 passo a mais: log2(2n) = log2 n + 1.
"""
import math


def busca_binaria(lista, alvo, mostrar=False):
    """Devolve (indice ou None, passos). Exige lista ordenada."""
    baixo, alto = 0, len(lista) - 1
    passos = 0
    while baixo <= alto:
        passos += 1
        meio = (baixo + alto) // 2
        chute = lista[meio]
        if mostrar:
            print(f"  passo {passos}: baixo={baixo:<3} alto={alto:<3} meio={meio:<3} chute={chute}")
        if chute == alvo:
            return meio, passos
        if chute < alvo:
            baixo = meio + 1              # alvo so pode estar na metade da direita
        else:
            alto = meio - 1               # alvo so pode estar na metade da esquerda
    return None, passos                   # intervalo vazio: nao esta na lista


if __name__ == "__main__":
    lista = [3, 8, 12, 19, 25, 31, 37, 42, 49, 56]
    print("Lista ordenada:", lista)
    for alvo in (37, 3, 4):
        print(f"\nProcurando {alvo}:")
        idx, passos = busca_binaria(lista, alvo, mostrar=True)
        print(f"  resultado: indice={idx} em {passos} passos")

    print("\nPIOR CASO MEDIDO x TEORIA")
    print(f"{'n':>10} {'pior caso medido':>17} {'floor(log2 n)+1':>16} {'ceil(log2 n) [livro]':>21}")
    for n in (100, 128, 256, 1_000, 240_000, 1_000_000):
        lst = list(range(n))
        pior = max(busca_binaria(lst, alvo)[1] for alvo in (0, n - 1, -1))
        print(f"{n:>10} {pior:>17} {math.floor(math.log2(n)) + 1:>16} {math.ceil(math.log2(n)):>21}")
    print("\nDobrar n acrescenta apenas 1 passo: crescimento logaritmico, O(log n).")
