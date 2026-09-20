"""Gera Catalogo_Scripts.md a partir dos scripts em scripts/.

Cada script traz, na docstring, um cabecalho padronizado:
    [NN] Titulo
    Tema: ... | Complexidade: ... | Memória: ...
    Palavras-chave: a, b, c
    O que faz:            (bullets)
    Perguntas prováveis:  (linhas P: / R:)
    Uso: ...              (opcional)

O catalogo reune: indice de scripts, indice de perguntas, indice de palavras-chave e,
para cada script, cabecalho + codigo + SAIDA REAL (o script e executado aqui).
Uso: python gerar_catalogo.py
"""
import ast
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPTS = AQUI / "scripts"
SAIDA_MD = AQUI / "Catalogo_Scripts.md"
MAX_LINHAS_SAIDA = 70


# ----------------------------------------------------------------------------- leitura
def ler_script(caminho: Path):
    """Devolve (docstring, codigo sem a docstring)."""
    fonte = caminho.read_text(encoding="utf-8")
    modulo = ast.parse(fonte)
    doc = ast.get_docstring(modulo, clean=False) or ""
    primeiro = modulo.body[0]
    if isinstance(primeiro, ast.Expr) and isinstance(primeiro.value, ast.Constant) and isinstance(primeiro.value.value, str):
        codigo = "\n".join(fonte.splitlines()[primeiro.end_lineno:]).strip("\n")
    else:
        codigo = fonte
    return doc, codigo


def analisar_doc(doc: str):
    linhas = doc.strip("\n").splitlines()
    m = re.match(r"\[(\d+)\]\s*(.*)", linhas[0].strip())
    ident, titulo = m.group(1), m.group(2).strip()
    meta = {"Tema": "", "Complexidade": "", "Memória": "", "Palavras-chave": ""}
    descricao, perguntas, uso = [], [], ""
    secao = None
    for linha in linhas[1:]:
        s = linha.strip()
        if s.startswith("Tema:"):
            for parte in s.split("|"):
                chave, _, valor = parte.partition(":")
                meta[chave.strip()] = valor.strip()
        elif s.startswith("Palavras-chave:"):
            meta["Palavras-chave"] = s.partition(":")[2].strip()
        elif s.startswith("O que faz:"):
            secao = "desc"
        elif s.startswith("Perguntas prováveis:"):
            secao = "perg"
        elif s.startswith("Uso:"):
            uso = s.partition(":")[2].strip()
        elif secao == "desc" and s:
            descricao.append(s[2:].strip() if s.startswith("- ") else s)
        elif secao == "perg" and s:
            if s.startswith("P:"):
                perguntas.append([s[2:].strip(), ""])
            elif s.startswith("R:") and perguntas:
                perguntas[-1][1] = s[2:].strip()
            elif perguntas:                                  # continuacao de linha
                alvo = 1 if perguntas[-1][1] else 0
                perguntas[-1][alvo] += " " + s
    return ident, titulo, meta, descricao, perguntas, uso


def executar(caminho: Path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, caminho.name], cwd=SCRIPTS, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env, timeout=300)
    saida = r.stdout
    if r.returncode != 0:
        saida += "\n[ERRO]\n" + r.stderr
    linhas = saida.rstrip().splitlines()
    if len(linhas) > MAX_LINHAS_SAIDA:
        linhas = linhas[:MAX_LINHAS_SAIDA] + [f"... ({len(linhas) - MAX_LINHAS_SAIDA} linhas omitidas; rode o script para ver tudo)"]
    return "\n".join(linhas), r.returncode


def chave_ordem(texto: str):
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()


def celula(texto: str):
    """Escapa o | para nao quebrar a tabela em Markdown."""
    return texto.replace("|", "\\|")


# ----------------------------------------------------------------------------- montagem
def montar():
    entradas = []
    for caminho in sorted(SCRIPTS.glob("[0-9][0-9]_*.py")):
        doc, codigo = ler_script(caminho)
        ident, titulo, meta, descricao, perguntas, uso = analisar_doc(doc)
        saida, rc = executar(caminho)
        status = "OK" if rc == 0 else f"ERRO (codigo {rc})"
        print(f"  [{ident}] {caminho.name:<32} {status}")
        entradas.append(dict(id=ident, arquivo=caminho.name, titulo=titulo, meta=meta,
                             descricao=descricao, perguntas=perguntas, uso=uso, codigo=codigo, saida=saida))

    hoje = date.today().strftime("%d/%m/%Y")
    md = []
    md.append("---")
    md.append('title: "Catálogo de Scripts — Análise de Algoritmos"')
    md.append(f'subtitle: "{len(entradas)} scripts comentados, com perguntas prováveis e saída real · Prova com consulta de 22/09/2026"')
    md.append("lang: pt-BR")
    md.append("---")
    md.append("")
    md.append("> **Como achar o que precisa.** Use **Ctrl+F** neste arquivo (ou no PDF) com uma palavra-chave: "
              "o nome do algoritmo (`bubble`, `quicksort`, `memo`), um conceito (`pior caso`, `pivô`, `caso base`, "
              "`n dobra`) ou um trecho da pergunta. Os três índices abaixo apontam para o script certo. "
              "Cada script é um arquivo independente em `scripts/` e roda sozinho com `python scripts/NN_nome.py`; "
              "a saída mostrada aqui é a saída real dessa execução.")
    md.append(">")
    md.append("> No terminal, para procurar dentro dos scripts: `findstr /s /i \"palavra\" scripts\\*.py` (Windows) "
              "ou `grep -ril palavra scripts/` (Git Bash).")
    md.append("")

    # indice de scripts
    md.append("# Índice de scripts")
    md.append("")
    md.append("| # | Script | Tema | Complexidade | Palavras-chave |")
    md.append("|--|------------------|---------|----------|------------------------|")
    for e in entradas:
        md.append(f"| [{e['id']}](#s{e['id']}) | `{e['arquivo']}`<br>{celula(e['titulo'])} | {celula(e['meta']['Tema'])} | "
                  f"{celula(e['meta']['Complexidade'])} | {celula(e['meta']['Palavras-chave'])} |")
    md.append("")

    # indice de perguntas
    md.append("# Índice de perguntas prováveis")
    md.append("")
    md.append("| Pergunta | Script |")
    md.append("|------------------------------------------|----|")
    for e in entradas:
        for p, _ in e["perguntas"]:
            md.append(f"| {celula(p)} | [{e['id']}](#s{e['id']}) |")
    md.append("")

    # indice de palavras-chave (lista em colunas; cada item: palavra + scripts)
    md.append("# Índice de palavras-chave")
    md.append("")
    md.append("Procure a palavra (Ctrl+F) e vá ao script indicado.")
    md.append("")
    indice = {}
    for e in entradas:
        for k in e["meta"]["Palavras-chave"].split(","):
            k = k.strip()
            if k:
                indice.setdefault(k.lower(), set()).add(e["id"])
    md.append("::: {.colunas}")
    for k in sorted(indice, key=chave_ordem):
        refs = ", ".join(f"[{i}](#s{i})" for i in sorted(indice[k]))
        md.append(f"- **{k}** {refs}")
    md.append(":::")
    md.append("")

    # scripts
    md.append("# Scripts")
    md.append("")
    for e in entradas:
        m = e["meta"]
        md.append(f"## [{e['id']}] {e['titulo']} {{#s{e['id']}}}")
        md.append("")
        md.append(f"**Arquivo:** `scripts/{e['arquivo']}` · **Tema:** {m['Tema']} · "
                  f"**Complexidade:** {m['Complexidade']} · **Memória:** {m['Memória']}  ")
        md.append(f"**Palavras-chave:** {m['Palavras-chave']}")
        if e["uso"]:
            md.append(f"  \n**Uso:** `{e['uso']}`")
        md.append("")
        md.append("**O que o script faz**")
        md.append("")
        for d in e["descricao"]:
            md.append(f"- {d}")
        md.append("")
        md.append("**Perguntas prováveis**")
        md.append("")
        for i, (p, r) in enumerate(e["perguntas"], 1):
            md.append(f"> **P{i}.** {p}  ")
            md.append(f"> **R.** {r}")
            md.append(">")
        if md[-1] == ">":
            md.pop()
        md.append("")
        md.append("**Código**")
        md.append("")
        md.append("```python")
        md.append(e["codigo"])
        md.append("```")
        md.append("")
        md.append(f"**Saída de exemplo** (execução real em {hoje})")
        md.append("")
        md.append("```text")
        md.append(e["saida"])
        md.append("```")
        md.append("")
    SAIDA_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Catalogo gerado:", SAIDA_MD, f"({len(entradas)} scripts)")


if __name__ == "__main__":
    montar()
