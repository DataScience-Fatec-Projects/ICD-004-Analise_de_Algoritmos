#!/usr/bin/env python3
"""
ICD-004 - Analise de Algoritmos | Aula 03 - Atividade 01
=========================================================
Monta o PDF de entrega a partir dos dados produzidos por atividade01.py.

Le  : saida/resultados.json + saida/grafico_*.png
Gera: saida/Atividade01_Busca_Linear_vs_Binaria.pdf

Uso:
    python atividade01.py     # 1o: roda o experimento
    python gerar_pdf.py       # 2o: monta o PDF
"""

from __future__ import annotations

import inspect
import json
import math
import sys
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, Image, KeepTogether, ListFlowable,
                                ListItem, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle, XPreformatted)

BASE = Path(__file__).parent
DIR_SAIDA = BASE / "saida"
PDF = DIR_SAIDA / "Atividade01_Busca_Linear_vs_Binaria.pdf"

sys.path.insert(0, str(BASE))
import atividade01 as exp                                    # noqa: E402
from atividade01 import CENARIOS, buscar, fmt, fmt_razao      # noqa: E402

# ----------------------------------------------------------------------------
# Identificacao da entrega
# ----------------------------------------------------------------------------

DISCIPLINA = "ICD-004 - Análise de Algoritmos"
AULA = "Aula 03 - Atividade 01"
TITULO = "Pesquisa Linear (O(n)) vs Pesquisa Binária (O(log n))"
INTEGRANTES = ["Wellington Torres"]
PRAZO = "25 de agosto de 2026"

AZUL = colors.HexColor("#1f6feb")
AZUL_ESC = colors.HexColor("#0b3d91")
VERMELHO = colors.HexColor("#c0392b")
CINZA = colors.HexColor("#57606a")
CINZA_CLARO = colors.HexColor("#f3f4f6")
BORDA = colors.HexColor("#d0d7de")


# ----------------------------------------------------------------------------
# Fontes e estilos
# ----------------------------------------------------------------------------

def registrar_fontes() -> tuple[str, str, str, str]:
    """Registra DejaVu (vem com o matplotlib) para ter acento e simbolos
    matematicos. Cai para as fontes padrao do PDF se nao encontrar."""
    try:
        import matplotlib
        ttf = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
        mapa = {
            "DejaVu": "DejaVuSans.ttf",
            "DejaVu-Bold": "DejaVuSans-Bold.ttf",
            "DejaVu-Italic": "DejaVuSans-Oblique.ttf",
            "DejaVuMono": "DejaVuSansMono.ttf",
        }
        for nome, arquivo in mapa.items():
            pdfmetrics.registerFont(TTFont(nome, ttf / arquivo))
        pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu",
                                      bold="DejaVu-Bold",
                                      italic="DejaVu-Italic",
                                      boldItalic="DejaVu-Bold")
        return "DejaVu", "DejaVu-Bold", "DejaVu-Italic", "DejaVuMono"
    except Exception as erro:                       # pragma: no cover
        print(f"    aviso: usando fontes padrao ({erro})")
        return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"


FONTE, FONTE_B, FONTE_I, MONO = registrar_fontes()


def montar_estilos() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    e: dict[str, ParagraphStyle] = {}

    e["capa_titulo"] = ParagraphStyle(
        "capa_titulo", parent=base["Title"], fontName=FONTE_B, fontSize=21,
        leading=26, textColor=AZUL_ESC, alignment=TA_CENTER, spaceAfter=6)
    e["capa_sub"] = ParagraphStyle(
        "capa_sub", fontName=FONTE, fontSize=12.5, leading=17, textColor=CINZA,
        alignment=TA_CENTER)
    e["capa_meta"] = ParagraphStyle(
        "capa_meta", fontName=FONTE, fontSize=10, leading=15, textColor=CINZA,
        alignment=TA_CENTER)
    e["h1"] = ParagraphStyle(
        "h1", fontName=FONTE_B, fontSize=14, leading=18, textColor=AZUL_ESC,
        spaceBefore=16, spaceAfter=7)
    e["h2"] = ParagraphStyle(
        "h2", fontName=FONTE_B, fontSize=11.5, leading=15, textColor=AZUL,
        spaceBefore=11, spaceAfter=5)
    e["corpo"] = ParagraphStyle(
        "corpo", fontName=FONTE, fontSize=10, leading=15.2,
        alignment=TA_JUSTIFY, spaceAfter=7)
    e["nota"] = ParagraphStyle(
        "nota", fontName=FONTE, fontSize=8.6, leading=12.5, textColor=CINZA,
        alignment=TA_JUSTIFY, spaceAfter=6)
    e["codigo"] = ParagraphStyle(
        "codigo", fontName=MONO, fontSize=7.1, leading=9.3,
        textColor=colors.HexColor("#1f2328"), backColor=CINZA_CLARO,
        borderColor=BORDA, borderWidth=0.6, borderPadding=6,
        spaceBefore=4, spaceAfter=9)
    e["console"] = ParagraphStyle(
        "console", parent=e["codigo"], fontSize=7.4, leading=10.2,
        backColor=colors.HexColor("#0d1117"),
        textColor=colors.HexColor("#c9d1d9"), borderColor=colors.HexColor("#30363d"))
    e["destaque"] = ParagraphStyle(
        "destaque", fontName=FONTE, fontSize=10, leading=15,
        alignment=TA_JUSTIFY, backColor=colors.HexColor("#eef4ff"),
        borderColor=AZUL, borderWidth=0.8, borderPadding=8,
        spaceBefore=4, spaceAfter=10)
    e["legenda"] = ParagraphStyle(
        "legenda", fontName=FONTE_I, fontSize=8.4, leading=11.5,
        textColor=CINZA, alignment=TA_CENTER, spaceAfter=12)
    e["celula"] = ParagraphStyle(
        "celula", fontName=FONTE, fontSize=8.4, leading=11)
    return e


E = montar_estilos()


# ----------------------------------------------------------------------------
# Componentes reutilizaveis
# ----------------------------------------------------------------------------

LARGURA_UTIL = A4[0] - 4 * cm
LARGURA_FIG = 13.6 * cm   # menor que a util: mantem figura e texto na mesma pagina


def p(texto: str, estilo: str = "corpo") -> Paragraph:
    return Paragraph(texto, E[estilo])


def bullets(itens: list[str], estilo: str = "corpo") -> ListFlowable:
    return ListFlowable(
        [ListItem(p(i, estilo), leftIndent=14, value="circle") for i in itens],
        bulletType="bullet", bulletFontName=FONTE, bulletFontSize=7,
        leftIndent=12, spaceAfter=8, bulletColor=AZUL)


def rotulo_cenario(cenario: str) -> str:
    """Nome do cenario como aparece nas tabelas do PDF (com acentos)."""
    return (cenario.replace("1o", "1º").replace("ultimo", "último")
                   .replace("medio", "médio").replace("aleatorio", "aleatório"))


def acentuar(texto: str) -> str:
    """O script de experimento escreve em ASCII (console portatil); aqui o
    texto vai para o PDF, onde os acentos sao esperados."""
    mapa = {
        "aleatorios": "aleatórios", "binaria": "binária",
        "indice": "índice", "teorico": "teórico",
        "unitaria": "unitária", "<=": "≤",
        "floor(log2(n))+1": "⌊log₂(n)⌋+1",
    }
    for antes, depois in mapa.items():
        texto = texto.replace(antes, depois)
    return texto


def imagem(nome: str, legenda: str, largura=LARGURA_FIG):
    caminho = DIR_SAIDA / nome
    px_w, px_h = ImageReader(str(caminho)).getSize()
    img = Image(str(caminho), width=largura, height=largura * px_h / px_w)
    return KeepTogether([img, Spacer(1, 4), p(legenda, "legenda")])


def tabela(dados: list[list], larguras: list[float], destaque_ultima=False,
           alinhamento_esq=(0,)) -> Table:
    """Tabela padrao: cabecalho azul, zebra, grade fina."""
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="CENTER")
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL_ESC),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), FONTE_B),
        ("FONTNAME", (0, 1), (-1, -1), FONTE),
        ("FONTSIZE", (0, 0), (-1, -1), 7.9),
        ("LEADING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDA),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for col in alinhamento_esq:
        estilo.append(("ALIGN", (col, 0), (col, -1), "LEFT"))
    for linha in range(1, len(dados)):
        if linha % 2 == 0:
            estilo.append(("BACKGROUND", (0, linha), (-1, linha), CINZA_CLARO))
    if destaque_ultima:
        estilo += [("FONTNAME", (-1, 1), (-1, -1), FONTE_B),
                   ("TEXTCOLOR", (-1, 1), (-1, -1), AZUL_ESC)]
    t.setStyle(TableStyle(estilo))
    return t


def rodape(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(FONTE, 7.6)
    canvas.setFillColor(CINZA)
    canvas.setStrokeColor(BORDA)
    canvas.line(2 * cm, 1.45 * cm, A4[0] - 2 * cm, 1.45 * cm)
    canvas.drawString(2 * cm, 1.05 * cm, f"{DISCIPLINA}  |  {AULA}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.05 * cm, f"Página {doc.page}")
    canvas.restoreState()


# ----------------------------------------------------------------------------
# Blocos do documento
# ----------------------------------------------------------------------------

def bloco_capa(dados: dict) -> list:
    hoje = date.today().strftime("%d/%m/%Y")
    nomes = "<br/>".join(f"<b>{n}</b>" for n in INTEGRANTES)
    return [
        Spacer(1, 2.2 * cm),
        p(DISCIPLINA.upper(), "capa_meta"),
        Spacer(1, 0.4 * cm),
        p(TITULO, "capa_titulo"),
        Spacer(1, 0.2 * cm),
        HRFlowable(width="45%", thickness=1.2, color=AZUL, hAlign="CENTER"),
        Spacer(1, 0.5 * cm),
        p("Comparação de algoritmos de busca por contagem de passos "
          "e benchmark por tempo", "capa_sub"),
        Spacer(1, 2.0 * cm),
        p("Integrante" + ("s" if len(INTEGRANTES) > 1 else ""), "capa_meta"),
        Spacer(1, 0.15 * cm),
        p(nomes, "capa_sub"),
        Spacer(1, 1.6 * cm),
        tabela([
            ["Atividade", AULA],
            ["Prazo de entrega", PRAZO],
            ["Data de geração deste relatório", hoje],
            ["Maior lista testada", f"{fmt(dados['config']['tamanhos'][-1])} elementos"],
            ["Ambiente de execução", f"Python {dados['config']['python']} "
                                    f"(semente {dados['config']['semente']})"],
            ["Tempo total do experimento", f"{fmt(dados['duracao_total_s'], 2)} s"],
        ], [6.6 * cm, 8.4 * cm], alinhamento_esq=(0, 1)),
        Spacer(1, 1.4 * cm),
        p("Relatório reprodutível: todos os números deste documento foram medidos "
          "pelo script <font name='%s'>atividade01.py</font> e transcritos "
          "automaticamente por <font name='%s'>gerar_pdf.py</font>." % (MONO, MONO),
          "nota"),
        PageBreak(),
    ]


def bloco_objetivo(dados: dict) -> list:
    cfg = dados["config"]
    return [
        p("1. Objetivo", "h1"),
        p("Implementar o algoritmo de <b>pesquisa linear</b>, de complexidade "
          "O(n), e compará-lo com a <b>pesquisa binária</b>, de complexidade "
          "O(log n), demonstrando a diferença entre os dois por duas evidências "
          "independentes: a <b>quantidade de passos</b> efetivamente executados e "
          "o <b>tempo de execução medido</b> (benchmark por tempo), usando listas "
          "grandes.", "corpo"),

        p("2. Metodologia", "h1"),
        p("Cada algoritmo foi instrumentado para devolver, além do índice "
          "encontrado, o número de comparações que executou. Assim a contagem de "
          "passos não é uma estimativa teórica: é o valor real da execução.", "corpo"),
        bullets([
            "<b>Listas de teste:</b> " + ", ".join(fmt(n) for n in cfg["tamanhos"]) +
            " elementos, ordenadas e sem repetições (<font name='%s'>"
            "list(range(n))</font>) — a ordenação é pré-requisito da busca "
            "binária." % MONO,
            "<b>Cenários:</b> melhor caso (alvo na 1ª posição), pior caso com o "
            "alvo na última posição, pior caso com o alvo <b>ausente</b> da lista "
            f"e caso médio (média de {cfg['amostras_aleatorias']} alvos sorteados).",
            "<b>Medição de tempo:</b> <font name='%s'>time.perf_counter</font>, "
            "relógio monotônico de alta resolução. Cada medição repete a chamada "
            "até esgotar um orçamento de %s s e reporta a <b>mediana</b> das "
            "amostras — mais robusta a interferência do sistema operacional do que "
            "a média." % (MONO, fmt(cfg["orcamento_s"], 2)),
            "<b>Reprodutibilidade:</b> semente fixa "
            f"(<font name='{MONO}'>random.seed({cfg['semente']})</font>), "
            "de modo que uma nova execução sorteia exatamente os mesmos alvos.",
        ]),
        p("<b>Por que medir as duas coisas?</b> A contagem de passos isola o "
          "algoritmo: é a mesma em qualquer máquina. O tempo mede o efeito real, "
          "mas depende de CPU, cache e da linguagem. Quando as duas evidências "
          "apontam na mesma direção, a conclusão não é um artefato da máquina de "
          "teste.", "destaque"),
    ]


def bloco_implementacao() -> list:
    def fonte(func) -> str:
        texto = inspect.getsource(func).rstrip()
        return (texto.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;"))

    return [
        PageBreak(),
        p("3. Implementação", "h1"),
        p("3.1 Pesquisa linear — O(n)", "h2"),
        p("Percorre a lista do início ao fim comparando elemento por elemento. "
          "Não exige lista ordenada e para assim que encontra o alvo.", "corpo"),
        XPreformatted(fonte(exp.busca_linear), E["codigo"]),
        p("3.2 Pesquisa binária — O(log n)", "h2"),
        p("Compara o alvo com o elemento do meio e descarta a metade que "
          "comprovadamente não pode conter o alvo, repetindo o processo sobre a "
          "metade restante: n → n/2 → n/4 → … → 1.", "corpo"),
        XPreformatted(fonte(exp.busca_binaria), E["codigo"]),
    ]


def bloco_validacao(dados: dict) -> list:
    return [
        p("4. Validação de corretude", "h1"),
        p("Antes de comparar desempenho é preciso garantir que os dois "
          "algoritmos estão corretos — um algoritmo rápido e errado não serve de "
          "base de comparação. O script executa estas verificações a cada "
          "execução, e qualquer falha interrompe o experimento:", "corpo"),
        bullets([acentuar(linha.replace("OK: ", "")) for linha in dados["validacao"]]),
        p("A verificação do limite teórico é a mais relevante para esta "
          "atividade: ela confirma empiricamente que a busca binária nunca "
          "excede ⌊log₂(n)⌋ + 1 comparações.", "corpo"),
    ]


def bloco_passos(dados: dict) -> list:
    med, ns = dados["medicoes"], dados["config"]["tamanhos"]
    linhas = [["Cenário", "n", "Linear (passos)", "Binária (passos)", "Razão"]]
    for cenario in CENARIOS:
        for n in ns:
            l = buscar(med, "linear", cenario, n)["passos"]
            b = buscar(med, "binaria", cenario, n)["passos"]
            linhas.append([rotulo_cenario(cenario), fmt(n), fmt(l, 1),
                           fmt(b, 1), fmt_razao(l / b)])
    return [
        PageBreak(),
        p("5. Resultado 1 — quantidade de passos", "h1"),
        p("Comparações efetivamente contadas durante a execução (não estimadas). "
          "A coluna <i>Razão</i> mostra quantas vezes a linear faz mais passos "
          "que a binária.", "corpo"),
        tabela(linhas, [5.0 * cm, 2.3 * cm, 3.0 * cm, 2.9 * cm, 2.3 * cm],
               destaque_ultima=True),
        Spacer(1, 10),
        p("Nos três cenários em que o alvo não está no início, a razão cresce "
          "junto com n — é exatamente isso que separa O(n) de O(log n). No "
          "melhor caso a razão é menor que 1: a busca linear encontra o alvo em "
          "1 comparação, enquanto a binária ainda precisa afunilar até a "
          "primeira posição. Notação assintótica descreve o comportamento no "
          "crescimento, não garante vantagem em todo caso particular.", "corpo"),
        Spacer(1, 6),
        imagem("grafico_passos.png",
               "Figura 1 — Passos no pior caso (ambos os eixos em escala "
               "logarítmica). A curva da binária acompanha a reta teórica "
               "log₂(n)+1; a da linear cresce na mesma proporção que n."),
    ]


def bloco_tempo(dados: dict) -> list:
    med, ns = dados["medicoes"], dados["config"]["tamanhos"]
    linhas = [["Cenário", "n", "Linear (µs)", "Binária (µs)", "Speedup"]]
    for cenario in CENARIOS:
        for n in ns:
            l = buscar(med, "linear", cenario, n)["tempo_us"]
            b = buscar(med, "binaria", cenario, n)["tempo_us"]
            linhas.append([rotulo_cenario(cenario), fmt(n), fmt(l, 2),
                           fmt(b, 2), fmt_razao(l / b)])
    n_max = ns[-1]
    pior = "pior caso (alvo ausente)"
    t_lin = buscar(med, "linear", pior, n_max)["tempo_us"]
    t_bin = buscar(med, "binaria", pior, n_max)["tempo_us"]
    return [
        PageBreak(),
        p("6. Resultado 2 — benchmark por tempo", "h1"),
        p("Tempo mediano por busca, em microssegundos (µs = 10⁻⁶ s).", "corpo"),
        tabela(linhas, [5.0 * cm, 2.3 * cm, 3.0 * cm, 2.9 * cm, 2.3 * cm],
               destaque_ultima=True),
        Spacer(1, 10),
        p(f"No pior caso com {fmt(n_max)} elementos, a busca linear levou "
          f"<b>{fmt(t_lin, 2)} µs</b> ({fmt(t_lin / 1000, 1)} ms) contra "
          f"<b>{fmt(t_bin, 2)} µs</b> da binária — cerca de "
          f"<b>{fmt_razao(t_lin / t_bin)}</b> mais rápida. O tempo confirma o que "
          "a contagem de passos previu, o que descarta a hipótese de a diferença "
          "ser um efeito da máquina de teste.", "destaque"),
        imagem("grafico_tempo.png",
               "Figura 2 — Tempo mediano por busca. A linha da binária é "
               "praticamente horizontal: multiplicar a lista por 1.000 quase não "
               "altera seu tempo."),
        imagem("grafico_speedup.png",
               "Figura 3 — Ganho de tempo da binária sobre a linear no pior "
               "caso. A vantagem não é constante: ela cresce com o tamanho da "
               "lista."),
    ]


def bloco_ordenacao(dados: dict) -> list:
    o = dados["ordenacao"]
    k = math.ceil(o["equilibrio_consultas"])
    return [
        p("7. O preço do pré-requisito: ordenar a lista", "h1"),
        p("A busca binária só funciona sobre lista ordenada, e ordenar não é "
          "grátis: custa O(n log n), <b>mais</b> que uma única busca linear "
          "O(n). Medimos esse custo para responder à pergunta prática: a partir "
          "de quantas consultas vale a pena ordenar?", "corpo"),
        tabela([
            ["Operação (n = " + fmt(o["n"]) + ")", "Tempo medido", "Complexidade"],
            ["Ordenar a lista (list.sort — Timsort)",
             f"{fmt(o['tempo_ordenacao_us'], 2)} µs", "O(n log n)"],
            ["1 busca linear (caso médio)",
             f"{fmt(o['tempo_linear_us'], 2)} µs", "O(n)"],
            ["1 busca binária (caso médio)",
             f"{fmt(o['tempo_binaria_us'], 2)} µs", "O(log n)"],
        ], [8.0 * cm, 4.0 * cm, 3.5 * cm], alinhamento_esq=(0,)),
        Spacer(1, 10),
        p("O ponto de equilíbrio k sai da desigualdade “k buscas lineares "
          "custam mais que ordenar + k buscas binárias”:", "corpo"),
        XPreformatted("    k * t_linear   >   t_ordenacao + k * t_binaria\n"
                      "==> k              >   t_ordenacao / (t_linear - t_binaria)",
                      E["codigo"]),
        p(f"<b>k ≈ {fmt(o['equilibrio_consultas'], 1)} consultas.</b> Para menos "
          f"de ~{k} buscas em uma lista desordenada, a pesquisa linear é a "
          f"escolha certa. A partir de ~{k} consultas, ordenar uma única vez e "
          "usar a binária em todas as seguintes passa a ser mais barato — e a "
          "vantagem só aumenta daí em diante.", "destaque"),
        p("É por isso que a resposta “qual algoritmo é melhor?” depende do uso: "
          "busca única em dado desordenado favorece a linear; consultas "
          "repetidas na mesma base favorecem manter a base ordenada (ou "
          "indexada) e usar a binária.", "corpo"),
    ]


def bloco_respostas(dados: dict) -> list:
    med, ns = dados["medicoes"], dados["config"]["tamanhos"]
    n_max, pior = ns[-1], "pior caso (alvo ausente)"
    p_lin = buscar(med, "linear", pior, n_max)["passos"]
    p_bin = buscar(med, "binaria", pior, n_max)["passos"]
    t_lin = buscar(med, "linear", pior, n_max)["tempo_us"]
    t_bin = buscar(med, "binaria", pior, n_max)["tempo_us"]
    o = dados["ordenacao"]

    # Tabela do efeito de dobrar n
    dobras = [1_000, 2_000, 4_000, 8_000]
    tab_dobra = [["n", "Passos O(n)", "Passos O(log n)", "Efeito de dobrar n"]]
    for i, n in enumerate(dobras):
        efeito = "—" if i == 0 else "linear: ×2  |  binária: +1 passo"
        tab_dobra.append([fmt(n), fmt(n), str(math.floor(math.log2(n)) + 1), efeito])

    # Tabela de escala
    escala = [1_000, 1_000_000, 1_000_000_000]
    tab_escala = [["n", "O(n) — passos no pior caso", "O(log n) — passos no pior caso"]]
    for n in escala:
        tab_escala.append([fmt(n), fmt(n), str(math.floor(math.log2(n)) + 1)])

    exemplo = ("lista  = [7, 2, 9, 1, 5]      # NAO ordenada\n"
               "alvo   = 1                    # existe, no indice 3\n"
               "\n"
               "passo 1: meio = indice 2 -> valor 9 ; 1 < 9  -> descarta a DIREITA\n"
               "         espaco restante = [7, 2]\n"
               "passo 2: meio = indice 0 -> valor 7 ; 1 < 7  -> descarta a DIREITA\n"
               "         espaco restante = [] -> retorna -1  (NAO ENCONTRADO)\n"
               "\n"
               "Resultado ERRADO: o alvo estava na lista, no indice 3, mas foi\n"
               "descartado no passo 1 junto com a metade da direita.")

    return [
        PageBreak(),
        p("8. Respostas às questões", "h1"),

        p("8.1 Qual a diferença entre os dois algoritmos em termos de "
          "quantidade de passos no pior caso?", "h2"),
        p("No pior caso — alvo na última posição ou <b>ausente</b> da lista — a "
          "pesquisa linear precisa comparar <b>todos</b> os elementos: são "
          "exatamente <b>n passos</b>. A pesquisa binária, no mesmo pior caso, "
          "executa no máximo <b>⌊log₂(n)⌋ + 1 passos</b>, porque cada comparação "
          "elimina metade do espaço de busca restante; o número de divisões por 2 "
          "necessárias para reduzir n a 1 é justamente log₂(n).", "corpo"),
        p(f"Nos dados medidos, com uma lista de {fmt(n_max)} elementos: "
          f"<b>{fmt(p_lin)} passos</b> na linear contra <b>{fmt(p_bin)} passos</b> "
          f"na binária — <b>{fmt_razao(p_lin / p_bin)} menos passos</b>, o que se "
          f"traduziu em {fmt(t_lin, 2)} µs contra {fmt(t_bin, 2)} µs de tempo "
          f"medido ({fmt_razao(t_lin / t_bin)} mais rápida). O limite teórico para "
          f"esse n é ⌊log₂({fmt(n_max)})⌋ + 1 = "
          f"{math.floor(math.log2(n_max)) + 1} passos, e a medição respeitou o "
          "limite.", "corpo"),
        p("Mais importante que o valor absoluto é <b>como cada um reage ao "
          "crescimento da lista</b>: dobrar n <b>dobra</b> o trabalho da busca "
          "linear, mas acrescenta <b>um único passo</b> à busca binária.", "corpo"),
        tabela(tab_dobra, [2.4 * cm, 2.9 * cm, 3.2 * cm, 7.0 * cm],
               alinhamento_esq=(3,)),
        Spacer(1, 12),

        p("8.2 Por que a busca binária exige que a lista esteja ordenada?", "h2"),
        p("Porque a busca binária <b>não usa a comparação para encontrar</b> o "
          "elemento, e sim para <b>decidir qual metade da lista pode ser "
          "descartada</b>. Quando ela conclui “o alvo é maior que o elemento do "
          "meio, logo só pode estar à direita”, está afirmando algo sobre "
          "elementos que <b>nunca olhou</b>. Essa inferência só é válida se a "
          "ordenação garantir o invariante: todo elemento à esquerda do meio é "
          "menor ou igual a ele, e todo elemento à direita é maior ou igual.", "corpo"),
        p("Sem ordenação, o invariante quebra e o algoritmo descarta uma metade "
          "que podia conter o alvo. O efeito não é ficar mais lento — é ficar "
          "<b>incorreto</b>, devolvendo “não encontrado” para um elemento que "
          "existe (falso negativo), o que é bem pior que ser lento, porque falha "
          "em silêncio:", "corpo"),
        XPreformatted(exemplo, E["codigo"]),
        p("Vale registrar o outro lado dessa exigência: a ordenação tem um "
          "custo, medido na seção 7. Ordenar a lista de "
          f"{fmt(o['n'])} elementos levou {fmt(o['tempo_ordenacao_us'], 2)} µs — "
          f"cerca de {fmt(o['tempo_ordenacao_us'] / o['tempo_linear_us'], 1)}× o "
          "custo de uma única busca linear. Por isso a binária só compensa quando "
          "a lista já está ordenada ou quando o custo da ordenação é amortizado "
          f"por muitas consultas (a partir de ~{math.ceil(o['equilibrio_consultas'])} "
          "neste experimento).", "corpo"),

        p("8.3 Escreva em suas palavras a diferença entre O(n) e O(log n).", "h2"),
        p("O(n) e O(log n) não são algoritmos nem “tipos de busca”: são "
          "<b>taxas de crescimento</b> — descrevem como o custo de um algoritmo "
          "aumenta conforme o tamanho da entrada (n) aumenta. A busca linear é "
          "<i>um exemplo</i> de O(n) e a binária é <i>um exemplo</i> de O(log n), "
          "mas a notação fala do comportamento, não da implementação.", "corpo"),
        bullets([
            "<b>O(n) — crescimento linear:</b> o trabalho cresce na mesma "
            "proporção que a entrada. O algoritmo precisa, no pior caso, olhar "
            "cada elemento uma vez. Lista 10× maior, trabalho 10× maior. É o "
            "custo inevitável quando não se pode assumir nada sobre a "
            "organização dos dados.",
            "<b>O(log n) — crescimento logarítmico:</b> cada passo <b>elimina uma "
            "fração fixa</b> do problema (na binária, metade). O trabalho cresce "
            "com o logaritmo da entrada: lista 10× maior custa apenas ~3,3 passos "
            "a mais; lista 1.000× maior, ~10 passos a mais. Só é possível porque "
            "o algoritmo explora uma estrutura pré-existente nos dados — a "
            "ordenação.",
        ]),
        p("A diferença fica evidente ao escalar n:", "corpo"),
        tabela(tab_escala, [3.2 * cm, 6.1 * cm, 6.2 * cm]),
        Spacer(1, 12),
        p("Em uma lista de 1 bilhão de elementos, o pior caso de O(n) é 1 bilhão "
          "de comparações, enquanto o de O(log n) são 30. Ou, invertendo a "
          "pergunta: com o orçamento de 30 comparações, O(log n) cobre 1 bilhão "
          "de elementos e O(n) cobre 30.", "destaque"),
        p("Duas observações que completam a resposta. <b>Primeira:</b> a notação "
          "Big O descreve o crescimento e ignora constantes, então ela não "
          "garante vantagem em <i>todo</i> caso — no melhor caso a busca linear "
          "acha o alvo em 1 passo, menos que a binária (seção 5). O que O(log n) "
          "garante é que a vantagem <b>aumenta</b> com n. <b>Segunda:</b> a base "
          "do logaritmo não aparece na notação porque mudar de base só multiplica "
          "o resultado por uma constante; escreve-se O(log n) mesmo quando o "
          "algoritmo divide o problema por 2, por 3 ou por 10.", "corpo"),
    ]


def bloco_conclusao(dados: dict) -> list:
    med, ns = dados["medicoes"], dados["config"]["tamanhos"]
    n_max, pior = ns[-1], "pior caso (alvo ausente)"
    t_lin = buscar(med, "linear", pior, n_max)["tempo_us"]
    t_bin = buscar(med, "binaria", pior, n_max)["tempo_us"]
    o = dados["ordenacao"]

    requisitos = [
        ["Requisito da atividade", "Onde foi atendido"],
        ["Implementar pesquisa linear O(n)", "Seção 3.1"],
        ["Comparar com pesquisa binária", "Seções 3.2, 5 e 6"],
        ["Provar a quantidade de passos", "Seção 5 (contagem instrumentada)"],
        ["Provar a eficiência em tempo (benchmark)", "Seção 6 (mediana, perf_counter)"],
        ["Usar uma lista grande", f"até {fmt(n_max)} elementos"],
        ["Responder às 3 questões", "Seções 8.1, 8.2 e 8.3"],
        ["Nome de todos no documento", "Capa"],
    ]
    return [
        PageBreak(),
        p("9. Conclusão", "h1"),
        bullets([
            f"<b>Passos:</b> no pior caso, linear = n e binária = ⌊log₂(n)⌋+1. "
            f"Com n = {fmt(n_max)}, isso é {fmt(n_max)} contra "
            f"{math.floor(math.log2(n_max)) + 1} comparações.",
            f"<b>Tempo:</b> a medição confirmou a previsão — {fmt(t_lin, 2)} µs "
            f"contra {fmt(t_bin, 2)} µs, {fmt_razao(t_lin / t_bin)} mais rápida no "
            "pior caso.",
            "<b>O ganho cresce com n:</b> a vantagem da binária não é um fator "
            "fixo; ela aumenta conforme a lista cresce (Figura 3). É essa "
            "propriedade que a notação assintótica captura.",
            "<b>Não é de graça:</b> a binária exige ordenação, que custa "
            f"O(n log n). Abaixo de ~{math.ceil(o['equilibrio_consultas'])} "
            "consultas sobre uma lista desordenada, a busca linear ainda é a "
            "escolha mais eficiente (seção 7).",
        ]),
        p("Escolher entre O(n) e O(log n), portanto, não é escolher o algoritmo "
          "“mais rápido” em abstrato: é verificar se os dados oferecem a "
          "estrutura (ordenação) que o algoritmo mais eficiente exige, e se o "
          "número de consultas justifica construir essa estrutura.", "corpo"),

        p("10. Requisitos da atividade", "h1"),
        tabela(requisitos, [8.5 * cm, 7.0 * cm], alinhamento_esq=(0, 1)),

        p("Apêndice — como reproduzir", "h1"),
        p("Os dois scripts estão no mesmo diretório deste PDF. Não há "
          "dependências além de <font name='%s'>matplotlib</font> (gráficos) e "
          "<font name='%s'>reportlab</font> (PDF):" % (MONO, MONO), "corpo"),
        XPreformatted("python atividade01.py     # roda o experimento -> saida/resultados.json + graficos\n"
                      "python gerar_pdf.py       # monta este PDF a partir do JSON",
                      E["console"]),
        p("A semente fixa garante que uma nova execução repita exatamente os "
          "mesmos alvos sorteados. Os tempos absolutos variam conforme a "
          "máquina, mas a razão entre os algoritmos e a forma das curvas se "
          "mantêm — é isso que a análise assintótica prevê.", "nota"),
    ]


# ----------------------------------------------------------------------------
def main() -> None:
    origem = DIR_SAIDA / "resultados.json"
    if not origem.exists():
        raise SystemExit("resultados.json não encontrado. "
                         "Rode primeiro: python atividade01.py")
    dados = json.loads(origem.read_text(encoding="utf-8"))

    doc = SimpleDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"{AULA} - {TITULO}",
        author=", ".join(INTEGRANTES), subject=DISCIPLINA,
    )

    historia: list = []
    for bloco in (bloco_capa(dados), bloco_objetivo(dados), bloco_implementacao(),
                  bloco_validacao(dados), bloco_passos(dados), bloco_tempo(dados),
                  bloco_ordenacao(dados), bloco_respostas(dados),
                  bloco_conclusao(dados)):
        historia.extend(bloco)

    doc.build(historia, onFirstPage=rodape, onLaterPages=rodape)
    tamanho_kb = PDF.stat().st_size / 1024
    print(f"PDF gerado: {PDF}")
    print(f"            {doc.page} páginas, {tamanho_kb:.0f} KB")


if __name__ == "__main__":
    main()
