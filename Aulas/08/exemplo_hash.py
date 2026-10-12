def funcao_hash(chave, tamanho):
    # Converter a chave em numero inteiro baseado na soma dos códigos de caractere
    return sum(ord(char) for char in chave) % tamanho
