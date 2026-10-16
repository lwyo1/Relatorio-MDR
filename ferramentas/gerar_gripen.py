"""Gera o relatório do caso de teste MDR-001 (Gripen) em saida/.

    python ferramentas/gerar_gripen.py
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from mdr import gerador, montagem  # noqa: E402
from tests.dados_gripen import base_gripen  # noqa: E402


def main():
    base = base_gripen()
    registro = base.registro("MDR-001")
    conteudo = montagem.montar(registro, base)
    saida = gerador.gerar(RAIZ / "modelos" / "relatorio_mdr.docx", conteudo,
                          RAIZ / "saida" / "Relatorio_MDR-001.docx")
    print("Relatório gerado em", saida)


if __name__ == "__main__":
    main()
