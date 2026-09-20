"""[16] Maior quadrado da fazenda (algoritmo de Euclides / MDC) — exemplo do livro e da aula 06
Tema: Dividir para conquistar / Recursividade | Complexidade: O(log(min(a, b))) | Memória: pilha O(log)
Palavras-chave: fazenda, 1680 x 640, maior quadrado, Euclides, MDC, resto da divisão, operador módulo, caso base múltiplo, dividir para conquistar, math.gcd, quadrado de 80

O que faz:
- Implementa maior_quadrado(lado1, lado2) da aula, imprimindo cada redução (lado1, lado2) -> (lado2, lado1 % lado2) até o caso base.
- Resolve a fazenda 1680 x 640 (resposta 80) e outros terrenos; confere com math.gcd e conta as chamadas.

Perguntas prováveis:
P: Qual é o caso base do problema da fazenda?
R: Quando um lado é múltiplo do outro (lado1 % lado2 == 0): o maior quadrado tem o lado menor. Ex.: 160 x 80 -> quadrados de 80.
P: Qual é o caso recursivo?
R: Preencher o retângulo com o maior quadrado possível e aplicar o mesmo algoritmo à sobra: maior_quadrado(lado2, lado1 % lado2). O maior quadrado que cabe na sobra é o maior que serve para o terreno inteiro.
P: Mostre as reduções para 1680 x 640.
R: (1680, 640) -> (640, 400) -> (400, 240) -> (240, 160) -> (160, 80) -> caso base. Resposta: 80 x 80 m, em 5 chamadas.
P: Que algoritmo clássico é esse?
R: O algoritmo de Euclides para o máximo divisor comum: MDC(1680, 640) = 80. Em Python, math.gcd(1680, 640).
P: Por que a complexidade é logarítmica?
R: A cada duas chamadas o menor lado pelo menos cai pela metade, então o número de passos cresce como log do menor lado.
"""
import math

chamadas = 0


def maior_quadrado(lado1, lado2, mostrar=True):
    global chamadas
    chamadas += 1
    if mostrar:
        print(f"  maior_quadrado({lado1}, {lado2})", end="")
    if lado1 == 0 or lado2 == 0:
        if mostrar:
            print(" -> 0")
        return 0
    if lado1 % lado2 == 0:                        # caso base: um lado e multiplo do outro
        if mostrar:
            print(f" -> {lado1} e multiplo de {lado2}: CASO BASE, quadrado de {lado2}")
        return lado2
    if mostrar:
        print(f" -> sobra {lado1} % {lado2} = {lado1 % lado2}")
    return maior_quadrado(lado2, lado1 % lado2, mostrar)   # reduz o problema


if __name__ == "__main__":
    terrenos = [(1680, 640), (1200, 450), (1071, 462), (100, 75), (25, 50)]
    for a, b in terrenos:
        chamadas = 0
        print(f"\nTerreno {a} x {b}:")
        r = maior_quadrado(a, b)
        print(f"  => quadrados de {r} x {r} | chamadas={chamadas} | math.gcd={math.gcd(a, b)}")
