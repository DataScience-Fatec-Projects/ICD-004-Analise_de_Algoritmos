"""
ICD-004 - Analise de Algoritmos
Aula 03 - Atividade 01

Monta o PDF de entrega usando os arquivos gerados pelo outro script.

Le  : busca_linear_vs_binaria.py, resultado.txt, tempos.csv
Gera: Atividade01_Busca_Linear_vs_Binaria.pdf

Para rodar:  python gerar_pdf.py
"""

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
SCRIPT = PASTA / "busca_linear_vs_binaria.py"
PDF = PASTA / "Atividade01_Busca_Linear_vs_Binaria.pdf"

NOMES = "Wellington Junior Torres de Melo"
DISCIPLINA = "ICD-004 - Análise de Algoritmos"
AULA = "Aula 03 - Atividade 01"

AZUL = colors.HexColor("#0b3d91")
CINZA = colors.HexColor("#f2f2f2")
BORDA = colors.HexColor("#cccccc")

# ---------------------------------------------------------------------------
# Estilos de texto
# ---------------------------------------------------------------------------
TITULO = ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=16,
                        leading=20, textColor=AZUL, spaceAfter=4)
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


def ler_tempos():
    """Le o tempos.csv e devolve uma lista de linhas [execucao, linear, binaria]."""
    linhas = (PASTA / "tempos.csv").read_text(encoding="utf-8").splitlines()
    dados = []
    for linha in linhas[1:]:                    # pula o cabecalho
        execucao, linear, binaria = linha.split(",")
        dados.append([execucao, float(linear), float(binaria)])
    return dados


def tabela_de_tempos(dados):
    """Monta a tabela comparativa: 1o resultado (linear) x 2o resultado (binaria)."""
    cabecalho = ["Execução", "1º resultado\nBusca linear - O(n)",
                 "2º resultado\nBusca binária - O(log n)",
                 "Quantas vezes\nmais rápida"]
    linhas = [cabecalho]

    for execucao, linear, binaria in dados:
        linhas.append([execucao, f"{linear:.4f} ms", f"{binaria:.4f} ms",
                       f"{linear / binaria:.0f}x"])

    media_linear = sum(d[1] for d in dados) / len(dados)
    media_binaria = sum(d[2] for d in dados) / len(dados)
    linhas.append(["Média", f"{media_linear:.4f} ms", f"{media_binaria:.4f} ms",
                   f"{media_linear / media_binaria:.0f}x"])

    tabela = Table(linhas, colWidths=[2.2 * cm, 4.6 * cm, 4.9 * cm, 3.3 * cm],
                   hAlign="CENTER")
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),   # linha da media
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8f0fe")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tabela


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, f"{DISCIPLINA}  |  {AULA}  |  {NOMES}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def main():
    dados = ler_tempos()
    media_linear = sum(d[1] for d in dados) / len(dados)
    media_binaria = sum(d[2] for d in dados) / len(dados)
    vezes = f"{media_linear / media_binaria:.0f}"

    conteudo = []

    # -------------------------------------------------------- identificação
    conteudo.append(Paragraph("Atividade 01 — Busca linear x Busca binária",
                              TITULO))
    conteudo.append(Paragraph(
        f"{DISCIPLINA}<br/>{AULA}<br/>"
        f"Aluno: <b>{NOMES}</b><br/>"
        f"Data: {date.today().strftime('%d/%m/%Y')}", SUBTITULO))

    # ---------------------------------------------------------- 1. o teste
    conteudo.append(Paragraph("1. O que foi testado", SECAO))
    conteudo.append(Paragraph(
        "Foram implementados dois algoritmos de busca em Python e o tempo de "
        "cada um foi medido com <b>time.perf_counter()</b>. O teste usa uma "
        "lista grande, com <b>1.000.000 de números ordenados</b> (de 0 a "
        "999.999), e procura o <b>último número da lista</b> — que é o pior "
        "caso para a busca linear, porque ela precisa passar por todos os "
        "elementos antes de achar. O teste foi repetido <b>3 vezes</b> para "
        "mostrar que o resultado não foi sorte de uma execução.", CORPO))

    # ------------------------------------------- 2. resultado por tempo
    conteudo.append(Paragraph("2. Resultado por tempo de cada execução", SECAO))
    conteudo.append(Paragraph(
        "Em cada execução aparecem dois resultados: o <b>1º resultado</b> é o "
        "tempo da busca linear e o <b>2º resultado</b> é o tempo da busca "
        "binária procurando exatamente o mesmo número, na mesma lista.", CORPO))
    conteudo.append(Spacer(1, 4))
    conteudo.append(tabela_de_tempos(dados))
    conteudo.append(Spacer(1, 12))
    conteudo.append(Paragraph(
        f"<b>Conclusão do teste:</b> a busca binária foi cerca de <b>{vezes} "
        f"vezes mais rápida</b> que a busca linear (média de "
        f"{media_binaria:.4f} ms contra {media_linear:.4f} ms). O motivo "
        "aparece na contagem de passos: a busca linear fez <b>1.000.000 de "
        "comparações</b> e a busca binária fez apenas <b>20</b>, porque cada "
        "passo dela joga fora metade da lista.", CORPO))

    # ----------------------------------------------- 3. saída do programa
    conteudo.append(Paragraph("3. Saída completa do programa", SECAO))
    conteudo.append(XPreformatted(
        (PASTA / "resultado.txt").read_text(encoding="utf-8"), CODIGO))

    # ---------------------------------------------------- 4. respostas
    conteudo.append(Paragraph("4. Respostas das questões", SECAO))

    conteudo.append(Paragraph(
        "<b>a) Qual a diferença entre os dois algoritmos em termos de "
        "quantidade de passos no pior caso?</b>", CORPO))
    conteudo.append(Paragraph(
        "No pior caso a busca linear precisa olhar todos os elementos, ou seja, "
        "<b>n passos</b> (no teste: 1.000.000). A busca binária corta a lista "
        "no meio a cada passo, então ela precisa de <b>log2(n) passos</b> (no "
        "teste: 20). A diferença mais importante é o que acontece quando a "
        "lista cresce: se eu dobrar o tamanho da lista, a busca linear passa a "
        "fazer o dobro de passos, enquanto a busca binária faz apenas <b>1 "
        "passo a mais</b>.", CORPO))

    conteudo.append(Paragraph(
        "<b>b) Por que a busca binária exige que a lista esteja ordenada?</b>",
        CORPO))
    conteudo.append(Paragraph(
        "Porque ela compara o alvo com o elemento do meio para decidir "
        "<b>qual metade jogar fora</b>. Quando ela conclui “o alvo é maior que "
        "o meio, então ele está na direita”, ela está afirmando algo sobre "
        "elementos que nem olhou — e isso só é verdade se a lista estiver "
        "ordenada. Em uma lista desordenada ela jogaria fora a metade que "
        "continha o alvo e diria que o número não existe. Ou seja, sem "
        "ordenação ela não fica lenta: ela fica <b>errada</b>.", CORPO))

    conteudo.append(Paragraph(
        "<b>c) Escreva em suas palavras a diferença entre O(n) e O(log n).</b>",
        CORPO))
    conteudo.append(Paragraph(
        "O(n) e O(log n) não são algoritmos: são formas de dizer <b>como o "
        "trabalho cresce</b> quando a entrada cresce. Em <b>O(n)</b> o trabalho "
        "cresce junto com a lista — lista 10 vezes maior, 10 vezes mais "
        "trabalho; é o caso da busca linear, que pode ter que olhar tudo. Em "
        "<b>O(log n)</b> cada passo elimina metade do que sobrou, então o "
        "trabalho cresce muito devagar — lista 1.000 vezes maior custa apenas "
        "cerca de 10 passos a mais; é o caso da busca binária. Em uma lista de "
        "1 bilhão de números, o pior caso de O(n) são 1 bilhão de comparações e "
        "o de O(log n) são 30 comparações.", CORPO))

    # --------------------------------------------------------- 5. código
    conteudo.append(PageBreak())
    conteudo.append(Paragraph("5. Script usado no teste", SECAO))
    conteudo.append(Paragraph(
        "Arquivo <b>busca_linear_vs_binaria.py</b> — é este script que faz as "
        "buscas e mede os tempos mostrados na seção 2.", CORPO))
    codigo = (SCRIPT.read_text(encoding="utf-8")
              .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    conteudo.append(XPreformatted(codigo, CODIGO))

    documento = SimpleDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"{AULA} - Busca linear x Busca binária", author=NOMES)
    documento.build(conteudo, onFirstPage=rodape, onLaterPages=rodape)

    print(f"PDF gerado: {PDF}")
    print(f"            {documento.page} paginas")


if __name__ == "__main__":
    main()
