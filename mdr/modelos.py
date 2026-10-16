"""Estrutura interna dos dados, independente da planilha.

A leitura do Excel (leitura.py) produz estes objetos; o resto do sistema só
conhece estes objetos. Assim, mudar a planilha afeta apenas a leitura.
"""

from dataclasses import dataclass, field


@dataclass
class Fonte:
    """Uma evidência de suporte (aba FONTES): 1 registro -> N evidências."""
    id_evidencia: str
    id_registro: str
    fonte: str
    evidencia: str
    tipo: str


@dataclass
class Limitacao:
    """Uma limitação/indeterminação (aba LIMITACOES)."""
    id_limitacao: str
    id_registro: str
    elemento: str
    situacao: str


@dataclass
class Lacuna:
    """Uma lacuna (aba LACUNAS); os vínculos N↔N ficam em registros."""
    id_lacuna: str
    descricao: str
    registros: list[str] = field(default_factory=list)


@dataclass
class Acao:
    """Uma ação do plano de ação (aba PLANO_ACAO)."""
    id_acao: str
    registros: list[str] = field(default_factory=list)
    lacunas: list[str] = field(default_factory=list)
    campos: dict = field(default_factory=dict)  # problema, objetivo, acao, ...


@dataclass
class Registro:
    """Um registro MDR: os valores ficam num dicionário pelas chaves de campos.py."""
    valores: dict

    @property
    def id(self) -> str:
        return str(self.valores.get("id_registro") or "").strip()

    def get(self, chave: str):
        return self.valores.get(chave)


@dataclass
class Base:
    """Tudo o que foi lido da planilha."""
    registros: list[Registro] = field(default_factory=list)
    fontes: list[Fonte] = field(default_factory=list)
    limitacoes: list[Limitacao] = field(default_factory=list)
    lacunas: list[Lacuna] = field(default_factory=list)
    acoes: list[Acao] = field(default_factory=list)
    # Aba FASES: (programa, fase) -> período (item 1.5).
    fases: dict[tuple[str, str], str] = field(default_factory=dict)
    # Aba TRAJETORIA: (programa, fase, função) -> classificação validada (item 8.1).
    trajetorias: dict[tuple[str, str, str], str] = field(default_factory=dict)
    # Problemas de estrutura encontrados na leitura (colunas ausentes, IDs repetidos...).
    avisos: list[str] = field(default_factory=list)

    def registro(self, id_registro: str) -> Registro:
        for r in self.registros:
            if r.id == id_registro:
                return r
        raise KeyError(f"Registro {id_registro} não encontrado na planilha.")

    def fontes_de(self, id_registro: str) -> list[Fonte]:
        return [f for f in self.fontes if f.id_registro == id_registro]

    def limitacoes_de(self, id_registro: str) -> list[Limitacao]:
        return [x for x in self.limitacoes if x.id_registro == id_registro]

    def lacunas_de(self, id_registro: str) -> list[Lacuna]:
        return [x for x in self.lacunas if id_registro in x.registros]

    def acoes_de(self, id_registro: str) -> list[Acao]:
        return [x for x in self.acoes if id_registro in x.registros]
