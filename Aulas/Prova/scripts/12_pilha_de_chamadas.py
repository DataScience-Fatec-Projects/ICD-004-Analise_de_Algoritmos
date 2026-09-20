"""[12] Pilha de chamadas: o exemplo greet / greet2 do livro (cap. 3)
Tema: Recursividade / Pilha | Complexidade: O(1) | Memória: pilha proporcional às chamadas aninhadas
Palavras-chave: pilha de chamadas, call stack, push, pop, greet, greet2, bye, chamada incompleta, suspensa, LIFO, livro 3.1

O que faz:
- Reproduz greet(name), que chama greet2 e bye, imprimindo o estado da pilha a cada entrada e saída de função.
- Mostra que greet fica "incompleta" enquanto greet2 executa, e é retomada depois.

Perguntas prováveis:
P: O que a pilha de chamadas guarda?
R: Um quadro por chamada em andamento, com as variáveis locais dela e o ponto de retorno. A última função chamada fica no topo e é a primeira a sair (LIFO).
P: Olhando a pilha [greet2 | name: maggie] sobre [greet | name: maggie], o que se conclui? (Livro, ex. 3.1)
R: greet foi chamada primeiro com name = maggie; ela chamou greet2 com o mesmo name; greet está suspensa esperando greet2 terminar; quando greet2 retornar, greet continua de onde parou.
P: Qual é a relação entre pilha de chamadas e recursão?
R: Cada chamada recursiva empilha um novo quadro; a profundidade da recursão é a altura da pilha. Sem caso base a pilha cresce sem limite (stack overflow).
"""

pilha = []


def empilhar(funcao, **variaveis):
    pilha.append((funcao, variaveis))
    print(f"  push {funcao}{variaveis}  ->  pilha: {[f for f, _ in pilha]}")


def desempilhar():
    funcao, _ = pilha.pop()
    print(f"  pop  {funcao}  ->  pilha: {[f for f, _ in pilha]}")


def greet2(name):
    empilhar("greet2", name=name)
    print(f"    how are you, {name}?")
    desempilhar()


def bye():
    empilhar("bye")
    print("    ok bye!")
    desempilhar()


def greet(name):
    empilhar("greet", name=name)
    print(f"    hello, {name}!")
    greet2(name)                       # greet fica suspensa aqui ate greet2 voltar
    print("    getting ready to say bye...")
    bye()
    desempilhar()


if __name__ == "__main__":
    print("greet('maggie'):")
    greet("maggie")
    print("\nA pilha volta a ficar vazia:", pilha)
