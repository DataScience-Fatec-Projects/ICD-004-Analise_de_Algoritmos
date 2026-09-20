"""[17] Reconhecendo o Big O de trechos de código: O(1), O(log n), O(n), O(n log n), O(n²), O(2^n)
Tema: Big O | Complexidade: uma função para cada classe | Memória: O(1) (exceto a exponencial, pilha O(n))
Palavras-chave: big o, classes de complexidade, contar operações, laço duplo, dividir por 2, n dobra, fator, constante, logarítmico, linear, linearítmico, quadrático, exponencial, subconjuntos, identificar complexidade

O que faz:
- Define seis funções, uma por classe de complexidade, cada uma contando suas operações.
- Executa cada uma para n e para 2n e imprime o fator de crescimento, que é a "assinatura" da classe.

Perguntas prováveis:
P: Como identificar o Big O de um trecho de código?
R: Conte quantas vezes a operação mais interna executa em função de n: um laço de 0 a n -> O(n); dois laços aninhados -> O(n²); um laço que divide n por 2 a cada volta -> O(log n); laço de n voltas com um interno logarítmico -> O(n log n); um número fixo de operações -> O(1).
P: Qual é o fator de crescimento de cada classe quando n dobra?
R: O(1): 1x; O(log n): +1 operação; O(n): 2x; O(n log n): pouco mais que 2x; O(n²): 4x; O(2^n): elevado ao quadrado.
P: for i in range(n): for j in range(i+1, n): ... é O(n²)?
R: Sim: são n(n-1)/2 pares, e a constante 1/2 é ignorada. É o padrão do selection sort e do bubble sort.
P: Um laço que faz i = i // 2 até i chegar a 1 é O(?)
R: O(log n): o número de voltas é o número de vezes que n pode ser dividido por 2, como na busca binária.
"""


def constante(n):                    # O(1): nao depende de n
    ops = 0
    primeiro = n; ops += 1
    ultimo = n * 2; ops += 1
    return ops


def logaritmico(n):                  # O(log n): divide por 2 a cada volta
    ops = 0
    i = n
    while i > 1:
        i //= 2; ops += 1
    return ops


def linear(n):                       # O(n): um laco
    ops = 0
    for _ in range(n):
        ops += 1
    return ops


def linearitmico(n):                 # O(n log n): laco externo n x interno log n
    ops = 0
    for _ in range(n):
        j = 1
        while j < n:
            j *= 2; ops += 1
    return ops


def quadratico(n):                   # O(n^2): dois lacos aninhados (pares i<j: n(n-1)/2)
    ops = 0
    for i in range(n):
        for j in range(i + 1, n):
            ops += 1
    return ops


def exponencial(n):                  # O(2^n): todos os subconjuntos de n itens
    ops = 0

    def gerar(i, escolhidos):
        nonlocal ops
        ops += 1
        if i == n:
            return
        gerar(i + 1, escolhidos)                 # sem o item i
        gerar(i + 1, escolhidos + [i])           # com o item i

    gerar(0, [])
    return ops


if __name__ == "__main__":
    casos = [
        ("O(1)", constante, 1024),
        ("O(log n)", logaritmico, 1024),
        ("O(n)", linear, 1024),
        ("O(n log n)", linearitmico, 1024),
        ("O(n^2)", quadratico, 1024),
        ("O(2^n)", exponencial, 10),
    ]
    print(f"{'classe':<11} {'n':>6} {'ops(n)':>10} {'ops(2n)':>10} {'fator':>8}   assinatura")
    print("-" * 70)
    assinaturas = {
        "O(1)": "nao muda", "O(log n)": "+1 operacao", "O(n)": "dobra (2x)",
        "O(n log n)": "pouco mais que 2x", "O(n^2)": "quadruplica (4x)", "O(2^n)": "eleva ao quadrado",
    }
    for nome, f, n in casos:
        a, b = f(n), f(2 * n)
        print(f"{nome:<11} {n:>6} {a:>10} {b:>10} {b / a:>7.2f}x   {assinaturas[nome]}")
