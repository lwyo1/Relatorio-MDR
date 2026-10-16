"""Os três estados que a especificação manda nunca confundir.

- NAO_DETERMINADO: a pesquisadora analisou e as evidências não bastam.
- NAO_APLICAVEL:   a dimensão não se aplica ao registro.
- VAZIO:           a célula ainda não foi preenchida (gera alerta; nunca vira
                   "Não determinado" nem grau D).

Só valores que sejam exatamente uma dessas expressões são reconhecidos.
Um texto livre como "Não determinado por este registro..." é conteúdo da
pesquisadora e é reproduzido como está.
"""

import enum
import unicodedata
from datetime import date, datetime


class Estado(enum.Enum):
    VAZIO = "vazio"
    NAO_DETERMINADO = "nao_determinado"
    NAO_APLICAVEL = "nao_aplicavel"
    PREENCHIDO = "preenchido"


NAO_PREENCHIDO = "Não preenchido"
NAO_APLICAVEL_TEXTO = "Não aplicável ao registro analisado"

_SUFIXO_ND = {"m": "o", "f": "a", "mp": "os", "fp": "as"}

_FORMAS_ND = {
    "nao determinado", "nao determinada", "nao determinados", "nao determinadas",
}
_FORMAS_NA = {"nao aplicavel"}
_COMPLEMENTO_ND = " com as evidencias disponiveis"
_COMPLEMENTO_NA = " ao registro analisado"


def _normalizar(texto: str) -> str:
    """Minúsculas, sem acentos, espaços simples, sem ponto final."""
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return " ".join(sem_acento.lower().split()).rstrip(".").strip()


def como_texto(valor) -> str:
    """Converte o valor de uma célula em texto, sem alterar o conteúdo."""
    if valor is None:
        return ""
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def classificar(valor) -> Estado:
    texto = como_texto(valor)
    if not texto.strip():
        return Estado.VAZIO
    n = _normalizar(texto)
    if n in _FORMAS_ND or any(n == f + _COMPLEMENTO_ND for f in _FORMAS_ND):
        return Estado.NAO_DETERMINADO
    if n in _FORMAS_NA or any(n == f + _COMPLEMENTO_NA for f in _FORMAS_NA):
        return Estado.NAO_APLICAVEL
    return Estado.PREENCHIDO


def texto_nao_determinado(genero: str = "m") -> str:
    return f"Não determinad{_SUFIXO_ND[genero]} com as evidências disponíveis"


def apresentar(valor, genero: str = "m") -> str:
    """Texto que vai para o relatório, conforme o estado do valor."""
    estado = classificar(valor)
    if estado is Estado.VAZIO:
        return NAO_PREENCHIDO
    if estado is Estado.NAO_DETERMINADO:
        return texto_nao_determinado(genero)
    if estado is Estado.NAO_APLICAVEL:
        return NAO_APLICAVEL_TEXTO
    return como_texto(valor).strip()
