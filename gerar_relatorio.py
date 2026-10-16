"""Gera o relatório de um registro a partir da planilha de entrada.

Uso:
    python gerar_relatorio.py <planilha.xlsx> <ID do registro> [arquivo de saída .docx]

Exemplo:
    python gerar_relatorio.py modelos/planilha_mdr.xlsx MDR-001
"""

import sys
from pathlib import Path

from mdr import gerador, leitura, montagem

RAIZ = Path(__file__).resolve().parent
TEMPLATE = RAIZ / "modelos" / "relatorio_mdr.docx"


def gerar(planilha: Path, id_registro: str, saida: Path | None = None) -> tuple[Path, list[str]]:
    base = leitura.ler(planilha)
    registro = base.registro(id_registro)
    conteudo = montagem.montar(registro, base)
    saida = saida or RAIZ / "saida" / f"Relatorio_{id_registro}.docx"
    return gerador.gerar(TEMPLATE, conteudo, saida), base.avisos


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    planilha, id_registro = Path(argv[0]), argv[1].strip()
    saida = Path(argv[2]) if len(argv) > 2 else None
    try:
        caminho, avisos = gerar(planilha, id_registro, saida)
    except (leitura.ErroPlanilha, KeyError) as e:
        print("ERRO:", e.args[0] if e.args else e)
        return 1
    for a in avisos:
        print("AVISO:", a)
    print("Relatório gerado em", caminho)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
