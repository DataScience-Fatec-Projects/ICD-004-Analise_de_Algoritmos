"""Gera os PDFs da revisao a partir dos Markdowns.

Pipeline (para cada documento): .md --(pandoc)--> .html --(Microsoft Edge headless)--> .pdf
Antes, roda gerar_catalogo.py para montar Catalogo_Scripts.md a partir dos scripts em scripts/.
Uso: python gerar_pdf.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CSS = AQUI / "estilo.css"
DOCUMENTOS = [
    AQUI / "Revisao_Prova_Exercicios.md",
    AQUI / "Guia_Algoritmos.md",
    AQUI / "Catalogo_Scripts.md",
]

PANDOC = shutil.which("pandoc") or str(Path.home() / "AppData/Local/Pandoc/pandoc.exe")
EDGE_CANDIDATOS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def gerar_html(md: Path, html: Path):
    cmd = [
        PANDOC, str(md), "-f", "markdown", "-t", "html5",
        "--standalone", "--embed-resources",
        "--toc", "--toc-depth=2",
        "--css", str(CSS),
        "--metadata", "lang=pt-BR",
        "-o", str(html),
    ]
    subprocess.run(cmd, check=True)


def gerar_pdf(html: Path, pdf: Path):
    edge = next((c for c in EDGE_CANDIDATOS if Path(c).exists()), None)
    if edge is None:
        sys.exit("Microsoft Edge nao encontrado; abra o HTML no navegador e use Imprimir > Salvar como PDF.")
    perfil = tempfile.mkdtemp(prefix="edge_pdf_")
    cmd = [
        edge, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
        f"--user-data-dir={perfil}",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf}",
        html.as_uri(),
    ]
    subprocess.run(cmd, check=True, timeout=300)
    shutil.rmtree(perfil, ignore_errors=True)


def main():
    subprocess.run([sys.executable, str(AQUI / "gerar_catalogo.py")], check=True)
    for md in DOCUMENTOS:
        html = md.with_suffix(".html")
        pdf = md.with_suffix(".pdf")
        gerar_html(md, html)
        gerar_pdf(html, pdf)
        html.unlink(missing_ok=True)          # o HTML e so intermediario
        print("PDF gerado :", pdf.name, f"({pdf.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
