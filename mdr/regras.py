"""Regras determinísticas sobre os graus A–D.

O sistema só reproduz o grau atribuído pela pesquisadora e o converte na
legenda fixa. Nunca calcula média, grau geral ou qualquer agregado (item 9.7),
e nunca transforma vazio, "Não determinado" ou "Não aplicável" em D.
"""

import re
from dataclasses import dataclass

from . import textos
from .campos import DIMENSOES_GRAU
from .estados import (
    NAO_APLICAVEL_TEXTO, NAO_PREENCHIDO, Estado, classificar, como_texto,
    texto_nao_determinado,
)

LEGENDA_GRAU = {
    "A": "Evidência sustentada",
    "B": "Evidência parcialmente sustentada",
    "C": "Participação ou vínculo documentado",
    "D": "Evidência insuficiente",
}

# Aceita "A", "a", "A — Evidência sustentada", "A - ...", "A." etc.
_PADRAO_GRAU = re.compile(r"^\s*([A-Da-d])\s*(?:$|[—–\-:.)\s])")


@dataclass(frozen=True)
class GrauLido:
    codigo: str | None   # "A".."D" quando válido
    estado: Estado
    bruto: str

    @property
    def valido(self) -> bool:
        """False quando há texto preenchido que não é um grau A–D."""
        return not (self.estado is Estado.PREENCHIDO and self.codigo is None)


def ler_grau(valor) -> GrauLido:
    bruto = como_texto(valor).strip()
    estado = classificar(valor)
    if estado is not Estado.PREENCHIDO:
        return GrauLido(None, estado, bruto)
    m = _PADRAO_GRAU.match(bruto)
    return GrauLido(m.group(1).upper() if m else None, estado, bruto)


def grau_por_extenso(valor) -> str:
    """'A' -> 'A — Evidência sustentada' (formato dos blocos 4 a 8)."""
    g = ler_grau(valor)
    if g.codigo:
        return f"{g.codigo} — {LEGENDA_GRAU[g.codigo]}"
    if g.estado is Estado.VAZIO:
        return NAO_PREENCHIDO
    if g.estado is Estado.NAO_APLICAVEL:
        return NAO_APLICAVEL_TEXTO
    if g.estado is Estado.NAO_DETERMINADO:
        return texto_nao_determinado("m")
    return g.bruto  # valor inválido: reproduzido como está (o alerta aponta)


def linha_quadro(dimensao: str, valor) -> tuple[str, str, str]:
    """Uma linha do Quadro de força das evidências: (dimensão, grau, leitura)."""
    g = ler_grau(valor)
    if g.codigo:
        return (dimensao, g.codigo, LEGENDA_GRAU[g.codigo])
    if g.estado is Estado.NAO_APLICAVEL:      # item 9.10
        return (dimensao, "—", NAO_APLICAVEL_TEXTO)
    if g.estado is Estado.VAZIO:              # item 9.9
        return (dimensao, "—", NAO_PREENCHIDO)
    if g.estado is Estado.NAO_DETERMINADO:    # item 9.11
        return (dimensao, "—", texto_nao_determinado("m"))
    return (dimensao, g.bruto, "Grau fora do padrão A–D")


def quadro_forca(valores: dict) -> list[tuple[str, str, str]]:
    """As cinco linhas fixas do bloco 9, na ordem da especificação."""
    return [linha_quadro(dim, valores.get(chave)) for dim, chave in DIMENSOES_GRAU]


def leitura_gerencial(valor_grau_atividade) -> str:
    """Bloco 4: frase fixa + frase que varia SÓ conforme o grau da atividade."""
    g = ler_grau(valor_grau_atividade)
    if g.codigo:
        return f"{textos.LEITURA_GERENCIAL_FIXA} {textos.LEITURA_GERENCIAL_POR_GRAU[g.codigo]}"
    # Sem grau A–D a especificação não define segunda frase: fica só a fixa,
    # e o alerta de consistência aponta o problema.
    return textos.LEITURA_GERENCIAL_FIXA
