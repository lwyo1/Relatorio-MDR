"""Lê a planilha de entrada (.xlsx) e monta a Base.

- As colunas são achadas pelo NOME do cabeçalho (mdr/planilha.py), não pela posição.
- Nenhum valor é alterado: o texto da célula segue como está para a montagem.
- Problemas de estrutura (coluna ausente, ID repetido, evidência ligada a um ID
  inexistente...) viram avisos em Base.avisos; a leitura não para por causa deles.
- Só falta de arquivo ou da aba REGISTROS impede a leitura (ErroPlanilha).
"""

import re
from pathlib import Path

from openpyxl import load_workbook

from . import planilha as P
from .campos import CAMPOS
from .estados import _normalizar, como_texto
from .modelos import Acao, Base, Fonte, Lacuna, Limitacao, Registro


class ErroPlanilha(Exception):
    pass


def _texto(valor) -> str:
    return como_texto(valor).strip()


def _ids(valor) -> list[str]:
    """'MDR-001; MDR-003' -> ['MDR-001', 'MDR-003'] (aceita ; , ou quebra de linha)."""
    return [x.strip() for x in re.split(r"[;,\n]", como_texto(valor)) if x.strip()]


def _achar_cabecalho(ws, nomes: dict[str, list[str]]) -> tuple[int, dict[str, int]]:
    """Procura nas 5 primeiras linhas a que tem mais cabeçalhos conhecidos.

    nomes: atributo -> nomes aceitos. Retorna (linha, {atributo: coluna}).
    """
    procurados = {_normalizar(n): attr for attr, ns in nomes.items() for n in ns}
    melhor = (0, {})
    for linha in range(1, min(ws.max_row, 5) + 1):
        achados = {}
        for col in range(1, ws.max_column + 1):
            attr = procurados.get(_normalizar(_texto(ws.cell(linha, col).value)))
            if attr and attr not in achados:
                achados[attr] = col
        if len(achados) > len(melhor[1]):
            melhor = (linha, achados)
    return melhor


def _linhas(ws, linha_cab: int, colunas: dict[str, int]):
    """Linhas de dados abaixo do cabeçalho, pulando as totalmente vazias."""
    for n in range(linha_cab + 1, ws.max_row + 1):
        valores = {attr: ws.cell(n, col).value for attr, col in colunas.items()}
        if any(_texto(v) for v in valores.values()):
            yield n, valores


def _ler_registros(ws, base: Base):
    nomes = {k: [CAMPOS[k].rotulo] + P.ALIASES.get(k, []) for k in P.COLUNAS_REGISTROS}
    linha_cab, colunas = _achar_cabecalho(ws, nomes)
    if "id_registro" not in colunas:
        raise ErroPlanilha("A aba REGISTROS não tem a coluna 'ID do registro'.")
    for k in P.COLUNAS_REGISTROS:
        if k not in colunas:
            base.avisos.append(f"REGISTROS: coluna '{CAMPOS[k].rotulo}' não encontrada.")
    vistos = set()
    for n, valores in _linhas(ws, linha_cab, colunas):
        id_ = _texto(valores.get("id_registro"))
        if not id_:
            base.avisos.append(f"REGISTROS, linha {n}: há dados mas falta o ID do registro.")
            continue
        if id_ in vistos:
            base.avisos.append(f"REGISTROS, linha {n}: ID {id_} repetido; "
                               "foi mantida a primeira ocorrência.")
            continue
        vistos.add(id_)
        valores["id_registro"] = id_
        base.registros.append(Registro(valores))


def _ler_auxiliar(wb, nome: str, base: Base, obrigatoria: bool = False):
    if nome not in wb.sheetnames:
        if obrigatoria:
            base.avisos.append(f"Aba {nome} não encontrada.")
        return
    ws = wb[nome]
    nomes = {attr: [cab] for attr, cab in P.AUXILIARES[nome]}
    linha_cab, colunas = _achar_cabecalho(ws, nomes)
    for attr, cab in P.AUXILIARES[nome]:
        if attr not in colunas:
            base.avisos.append(f"{nome}: coluna '{cab}' não encontrada.")
    for n, v in _linhas(ws, linha_cab, colunas):
        yield n, v


def ler(caminho: str | Path) -> Base:
    caminho = Path(caminho)
    if not caminho.exists():
        raise ErroPlanilha(f"Arquivo não encontrado: {caminho}")
    try:
        wb = load_workbook(str(caminho), data_only=True)
    except Exception as e:  # arquivo corrompido, aberto em outro formato etc.
        raise ErroPlanilha(f"Não foi possível abrir a planilha: {e}") from e
    if P.REGISTROS not in wb.sheetnames:
        raise ErroPlanilha("A planilha não tem a aba REGISTROS.")

    base = Base()
    _ler_registros(wb[P.REGISTROS], base)
    ids = {r.id for r in base.registros}

    for n, v in _ler_auxiliar(wb, P.FONTES, base, obrigatoria=True):
        f = Fonte(_texto(v.get("id_evidencia")), _texto(v.get("id_registro")),
                  _texto(v.get("fonte")), _texto(v.get("evidencia")),
                  _texto(v.get("tipo")))
        if f.id_registro not in ids:
            base.avisos.append(f"FONTES, linha {n}: ID MDR '{f.id_registro}' não existe "
                               "na aba REGISTROS.")
        base.fontes.append(f)

    for n, v in _ler_auxiliar(wb, P.LIMITACOES, base, obrigatoria=True):
        x = Limitacao(_texto(v.get("id_limitacao")), _texto(v.get("id_registro")),
                      _texto(v.get("elemento")), _texto(v.get("situacao")))
        if x.id_registro not in ids:
            base.avisos.append(f"LIMITACOES, linha {n}: ID MDR '{x.id_registro}' não "
                               "existe na aba REGISTROS.")
        base.limitacoes.append(x)

    for n, v in _ler_auxiliar(wb, P.LACUNAS, base, obrigatoria=True):
        lac = Lacuna(_texto(v.get("id_lacuna")), _texto(v.get("descricao")),
                     _ids(v.get("registros")))
        for r in lac.registros:
            if r not in ids:
                base.avisos.append(f"LACUNAS, linha {n}: registro '{r}' não existe na "
                                   "aba REGISTROS.")
        base.lacunas.append(lac)

    for n, v in _ler_auxiliar(wb, P.PLANO_ACAO, base, obrigatoria=True):
        base.acoes.append(Acao(
            _texto(v.get("id_acao")), _ids(v.get("registros")), _ids(v.get("lacunas")),
            {k: v.get(k) for k, _ in P.CAMPOS_ACAO}))

    for n, v in _ler_auxiliar(wb, P.FASES, base, obrigatoria=True):
        base.fases[(_texto(v.get("programa")), _texto(v.get("fase")))] = \
            _texto(v.get("periodo"))

    for n, v in _ler_auxiliar(wb, P.TRAJETORIA, base, obrigatoria=True):
        chave = (_texto(v.get("programa")), _texto(v.get("fase")), _texto(v.get("funcao")))
        base.trajetorias[chave] = _texto(v.get("trajetoria"))

    return base
