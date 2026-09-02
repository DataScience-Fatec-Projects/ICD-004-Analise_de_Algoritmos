"""
ICD-004 - Analise de Algoritmos
Aula 04 - Atividade 02

Monta o PDF de entrega usando os arquivos gerados pelo outro script.

Le  : bubble_sort_ia.py, resultado.txt, operacoes.csv, cenarios.csv
Gera: Atividade02_Bubble_Sort_vs_Selection_Sort.pdf

Para rodar:  python bubble_sort_ia.py   (gera o resultado.txt e os dois .csv)
             python gerar_pdf.py
"""

import csv
import io
import tokenize
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle, XPreformatted)

PASTA = Path(__file__).parent
SCRIPT = PASTA / "bubble_sort_ia.py"
PDF = PASTA / "Atividade02_Bubble_Sort_vs_Selection_Sort.pdf"

NOMES = "Wellington Junior Torres de Melo"
DISCIPLINA = "ICD-004 - Análise de Algoritmos"
AULA = "Aula 04 - Atividade 02"

AZUL = colors.HexColor("#0b3d91")
CINZA = colors.HexColor("#f2f2f2")
BORDA = colors.HexColor("#cccccc")
DESTAQUE = colors.HexColor("#e8f0fe")

# ---------------------------------------------------------------------------
# Estilos de texto
# ---------------------------------------------------------------------------
TITULO = ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=15,
                        leading=19, textColor=AZUL, spaceAfter=4)
SUBTITULO = ParagraphStyle("subtitulo", fontName="Helvetica", fontSize=10,
                           leading=14, textColor=colors.HexColor("#555555"),
                           spaceAfter=14)
SECAO = ParagraphStyle("secao", fontName="Helvetica-Bold", fontSize=12.5,
                       leading=16, textColor=AZUL, spaceBefore=16, spaceAfter=6)
CORPO = ParagraphStyle("corpo", fontName="Helvetica", fontSize=10, leading=15,
                       alignment=TA_JUSTIFY, spaceAfter=6)
CODIGO = ParagraphStyle("codigo", fontName="Courier", fontSize=6.9, leading=8.8,
                        backColor=CINZA, borderColor=BORDA, borderWidth=0.6,
                        borderPadding=6, spaceBefore=4, spaceAfter=8)


def escapar(texto):
    """Deixa o texto seguro para o XPreformatted do reportlab."""
    return (texto.replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;"))


def milhar(numero):
    """Formata 124750 como 124.750."""
    return f"{numero:,}".replace(",", ".")


# O Helvetica padrao do reportlab usa WinAnsi, que nao tem estes glifos:
# se ficarem no texto eles saem em branco no PDF.
SEM_GLIFO = {"−": "-", "→": "—", "≈": "~", "×": "x"}


def paragrafo(texto, estilo):
    """Cria o Paragraph trocando os caracteres que a fonte padrao nao tem."""
    for original, substituto in SEM_GLIFO.items():
        texto = texto.replace(original, substituto)
    return Paragraph(texto, estilo)


def codigo_sem_comentarios(caminho):
    """Le o .py e devolve o codigo sem comentarios, para caber melhor no PDF.

    Usa o tokenize para achar os comentarios de verdade - assim um '#' que
    esteja dentro de uma string nunca e confundido com comentario.
    """
    fonte = caminho.read_text(encoding="utf-8")
    linhas = fonte.splitlines()

    # Corta cada linha na coluna onde comeca o comentario.
    for token in tokenize.generate_tokens(io.StringIO(fonte).readline):
        if token.type == tokenize.COMMENT:
            linha, coluna = token.start
            linhas[linha - 1] = linhas[linha - 1][:coluna].rstrip()

    # Tira as linhas que sobraram vazias e nunca deixa 2 brancos seguidos.
    limpas = []
    for linha in linhas:
        if linha.strip() == "" and (not limpas or limpas[-1] == ""):
            continue
        limpas.append(linha.rstrip())

    return "\n".join(limpas).strip()


def ler_csv(nome, colunas_inteiras):
    """Le um dos CSVs gerados pelo bubble_sort_ia.py."""
    texto = (PASTA / nome).read_text(encoding="utf-8")
    dados = list(csv.DictReader(io.StringIO(texto)))
    for registro in dados:
        for chave in colunas_inteiras:
            registro[chave] = int(registro[chave])
    return dados


CONTAGENS = ["bubble_comparacoes", "bubble_trocas",
             "selection_comparacoes", "selection_trocas"]


def estilo_base():
    """Estilo comum das duas tabelas."""
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ])


def tabela_cenarios(cenarios):
    """Os tres cenarios pedidos no enunciado (n = 5), bubble x selection."""
    # Quebra "Melhor caso (ja ordenada)" em duas linhas e devolve os acentos.
    acentos = {"ja ordenada": "já ordenada", "Medio": "Médio",
               "aleatoria": "aleatória", "Cenario": "Cenário"}

    linhas = [["Cenário", "Lista",
               "Bubble\ncomparações", "Bubble\ntrocas",
               "Selection\ncomparações", "Selection\ntrocas"]]

    for registro in cenarios:
        nome = registro["cenario"]
        for sem, com in acentos.items():
            nome = nome.replace(sem, com)
        linhas.append([nome.replace(" (", "\n("), registro["lista"],
                       str(registro["bubble_comparacoes"]),
                       str(registro["bubble_trocas"]),
                       str(registro["selection_comparacoes"]),
                       str(registro["selection_trocas"])])

    tabela = Table(linhas,
                   colWidths=[3.3 * cm, 3.0 * cm, 2.4 * cm, 1.9 * cm,
                              2.5 * cm, 1.9 * cm],
                   hAlign="CENTER")
    tabela.setStyle(estilo_base())
    return tabela


def tabela_crescimento(dados):
    """Como as operacoes crescem quando n aumenta."""
    linhas = [["n", "Cenário",
               "Bubble\ncomparações", "Bubble\ntrocas",
               "Selection\ncomparações", "Selection\ntrocas"]]

    for registro in dados:
        linhas.append([str(registro["n"]), registro["cenario"],
                       milhar(registro["bubble_comparacoes"]),
                       milhar(registro["bubble_trocas"]),
                       milhar(registro["selection_comparacoes"]),
                       milhar(registro["selection_trocas"])])

    tabela = Table(linhas,
                   colWidths=[1.4 * cm, 2.4 * cm, 2.8 * cm, 2.4 * cm,
                              2.9 * cm, 2.4 * cm],
                   hAlign="CENTER", repeatRows=1)
    estilo = estilo_base()
    # Uma faixa de fundo a cada bloco de 3 linhas (um n por bloco).
    for bloco in range(len(dados) // 3):
        if bloco % 2 == 1:
            inicio = 1 + bloco * 3
            estilo.add("BACKGROUND", (0, inicio), (-1, inicio + 2), DESTAQUE)
    tabela.setStyle(estilo)
    return tabela


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, f"{DISCIPLINA}  |  {AULA}  |  {NOMES}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def main():
    dados = ler_csv("operacoes.csv", ["n"] + CONTAGENS)
    cenarios = ler_csv("cenarios.csv", CONTAGENS)
    por_cenario = {(d["n"], d["cenario"]): d for d in dados}

    b_melhor = cenarios[0]
    b_pior = cenarios[2]
    pior_50 = por_cenario[(50, "pior")]["bubble_comparacoes"]
    pior_100 = por_cenario[(100, "pior")]["bubble_comparacoes"]
    melhor_500 = por_cenario[(500, "melhor")]["bubble_comparacoes"]
    pior_500 = por_cenario[(500, "pior")]["bubble_comparacoes"]
    medio_500_trocas = por_cenario[(500, "medio")]["bubble_trocas"]
    select_500_trocas = por_cenario[(500, "pior")]["selection_trocas"]

    conteudo = []

    # -------------------------------------------------------- identificação
    conteudo.append(paragrafo("Atividade 02 — Bubble Sort: contagem de "
                              "operações e comparação com o Selection Sort",
                              TITULO))
    conteudo.append(paragrafo(
        f"{DISCIPLINA}<br/>{AULA}<br/>"
        f"Aluno: <b>{NOMES}</b><br/>"
        f"Data: {date.today().strftime('%d/%m/%Y')}", SUBTITULO))

    # --------------------------------------------------- 1. o que foi feito
    conteudo.append(paragrafo("1. O que foi implementado", SECAO))
    conteudo.append(paragrafo(
        "Foram implementados em Python o <b>Bubble Sort</b> e o <b>Selection "
        "Sort</b>, os dois instrumentados para contar <b>comparações</b> e "
        "<b>trocas</b>. O Bubble Sort compara pares vizinhos e troca quando "
        "estão fora de ordem; a cada passagem o maior elemento restante "
        "“sobe” para o fim da lista, então a passagem seguinte já olha um "
        "elemento a menos. Quando uma passagem inteira não faz nenhuma troca, "
        "a lista já está ordenada e o algoritmo para — que é o item 3 do "
        "“Como funciona” do enunciado.", CORPO))
    conteudo.append(paragrafo(
        "Cada execução confere o resultado contra o <b>sorted()</b> antes de "
        "reportar os números, para garantir que a contagem se refere a uma "
        "ordenação de fato correta.", CORPO))

    # --------------------------------------------------- 2. os tres cenarios
    conteudo.append(paragrafo("2. Os três cenários com n = 5", SECAO))
    conteudo.append(paragrafo(
        "Cada cenário foi ordenado pelos dois algoritmos, sobre a mesma "
        "lista, contando comparações e trocas:", CORPO))
    conteudo.append(Spacer(1, 4))
    conteudo.append(tabela_cenarios(cenarios))
    conteudo.append(Spacer(1, 10))
    conteudo.append(paragrafo(
        f"O contraste já aparece com n = 5: o Bubble Sort vai de "
        f"<b>{b_melhor['bubble_comparacoes']} comparações</b> na lista já "
        f"ordenada para <b>{b_pior['bubble_comparacoes']}</b> na invertida, "
        f"enquanto o Selection Sort faz "
        f"<b>{b_pior['selection_comparacoes']} comparações nos três casos</b>. "
        f"Em compensação, no pior caso o Bubble Sort faz "
        f"<b>{b_pior['bubble_trocas']} trocas</b> contra apenas "
        f"<b>{b_pior['selection_trocas']}</b> do Selection Sort.", CORPO))

    # ----------------------------------------------------- 3. crescimento
    conteudo.append(PageBreak())
    conteudo.append(paragrafo("3. Crescimento das operações conforme o "
                              "tamanho da lista", SECAO))
    conteudo.append(paragrafo(
        "Para enxergar o comportamento assintótico, o mesmo teste foi "
        "repetido com listas maiores (a lista aleatória usa semente fixa, "
        "então o resultado é reprodutível):", CORPO))
    conteudo.append(Spacer(1, 4))
    conteudo.append(tabela_crescimento(dados))
    conteudo.append(Spacer(1, 10))
    conteudo.append(paragrafo(
        f"A tabela confirma o <b>O(n²)</b>: quando n dobra de 50 para 100, as "
        f"comparações do pior caso saem de <b>{milhar(pior_50)}</b> para "
        f"<b>{milhar(pior_100)}</b> — cerca de <b>4 vezes mais</b>, que é "
        f"exatamente o esperado de um algoritmo quadrático (2² = 4). Já o "
        f"melhor caso do Bubble Sort cresce de forma linear: com n = 500 são "
        f"apenas <b>{milhar(melhor_500)}</b> comparações (n − 1) contra "
        f"<b>{milhar(pior_500)}</b> no pior caso.", CORPO))

    # ------------------------------ 4. por que o numero de operacoes varia
    conteudo.append(paragrafo("4. Por que o número de operações varia", SECAO))
    conteudo.append(paragrafo(
        "O Bubble Sort só troca quando encontra um par vizinho fora de ordem, "
        "e só faz uma nova passagem se a anterior trocou alguma coisa. Ou "
        "seja: o trabalho dele depende de <b>quanto a lista já está "
        "ordenada</b>.", CORPO))
    conteudo.append(paragrafo(
        "<b>Melhor caso (lista ordenada):</b> a primeira passagem não troca "
        "nada, o algoritmo percebe isso pela bandeira de controle e para. Faz "
        "apenas <b>n − 1 comparações</b> e <b>0 trocas</b> — comportamento "
        "<b>O(n)</b>.", CORPO))
    conteudo.append(paragrafo(
        "<b>Pior caso (lista invertida):</b> todo par comparado está fora de "
        "ordem, então ele troca em <i>todas</i> as comparações e nunca "
        "consegue parar mais cedo. Faz <b>n(n−1)/2 comparações</b> e o mesmo "
        "número de trocas — <b>O(n²)</b>.", CORPO))
    conteudo.append(paragrafo(
        f"<b>Médio caso (lista aleatória):</b> fica entre os dois. Em média "
        f"metade dos pares está fora de ordem, então o número de trocas cai "
        f"perto da metade do pior caso — na tabela, com n = 500, foram "
        f"<b>{milhar(medio_500_trocas)}</b> trocas contra "
        f"<b>{milhar(pior_500)}</b> do pior caso. Ainda assim é <b>O(n²)</b>, "
        f"porque a notação descreve o <i>crescimento</i>, não o valor exato.",
        CORPO))

    # -------------------------------- 5. comparacao com o selection sort
    conteudo.append(paragrafo("5. Comparação com o Selection Sort", SECAO))
    conteudo.append(paragrafo(
        "O Selection Sort percorre <b>todo</b> o trecho que ainda falta "
        "ordenar para achar o menor elemento, sem aproveitar a ordem que já "
        "existe. Por isso ele faz <b>sempre n(n−1)/2 comparações</b>, nos "
        "três cenários: com n = 5 são 10 comparações tanto na lista ordenada "
        "quanto na invertida. Ele é <b>O(n²) inclusive no melhor caso</b> — "
        "não tem como parar antes.", CORPO))
    conteudo.append(paragrafo(
        f"Em compensação, faz no máximo <b>n − 1 trocas</b>, porque cada "
        f"elemento vai direto para a posição final. Com n = 500 no pior caso "
        f"foram <b>{milhar(select_500_trocas)}</b> trocas contra "
        f"<b>{milhar(pior_500)}</b> do Bubble Sort — quase três ordens de "
        f"grandeza de diferença em movimentação de dados.", CORPO))
    conteudo.append(paragrafo("<b>Resumindo, quando usar cada um:</b>", CORPO))
    conteudo.append(paragrafo(
        "• <b>Lista quase ordenada</b> → Bubble Sort, porque ele detecta isso "
        "e para em uma única passagem, O(n).<br/>"
        "• <b>Trocas caras</b> (registros grandes, gravação em disco) → "
        "Selection Sort, porque movimenta muito menos dados.<br/>"
        "• <b>Listas grandes</b> → nenhum dos dois: ambos são O(n²). Vale usar "
        "algoritmos O(n log n), como Merge Sort ou Quick Sort.", CORPO))

    # ------------------------------------------------ 6. saída do programa
    conteudo.append(PageBreak())
    conteudo.append(paragrafo("6. Saída completa do programa", SECAO))
    conteudo.append(XPreformatted(
        escapar((PASTA / "resultado.txt").read_text(encoding="utf-8")), CODIGO))

    # ------------------------------------------------------- 7. código
    conteudo.append(PageBreak())
    conteudo.append(paragrafo("7. Código-fonte", SECAO))
    conteudo.append(paragrafo(
        f"Arquivo <b>{SCRIPT.name}</b> — é este script que ordena, conta as "
        "operações e gera o resultado.txt e o operacoes.csv usados nas seções "
        "anteriores. Os comentários foram removidos aqui para o código caber "
        "melhor na página; o arquivo original está comentado.", CORPO))
    conteudo.append(XPreformatted(
        escapar(codigo_sem_comentarios(SCRIPT)), CODIGO))

    documento = SimpleDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"{AULA} - Bubble Sort x Selection Sort", author=NOMES)
    documento.build(conteudo, onFirstPage=rodape, onLaterPages=rodape)

    print(f"PDF gerado: {PDF}")
    print(f"            {documento.page} paginas")


if __name__ == "__main__":
    main()
