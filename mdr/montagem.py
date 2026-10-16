"""Monta o conteúdo de cada bloco do relatório a partir de um registro.

Saída: um dicionário {marcador: valor}. Valores são textos (campos simples)
ou listas de tuplas (linhas das tabelas dinâmicas). O gerador apenas encaixa
esse conteúdo no modelo Word; toda decisão de conteúdo acontece aqui.
"""

from datetime import datetime

from . import regras, textos
from .campos import CAMPOS
from .estados import NAO_PREENCHIDO, apresentar, como_texto
from .modelos import Base, Registro

# Campos reproduzidos diretamente (bloco -> lista de chaves).
_REPRODUCAO_DIRETA = [
    # bloco 1
    "id_registro", "programa", "fase_temporal", "funcao_tecnologica",
    "ator_focal", "tipo_ator", "parceiros", "status_analise", "responsavel",
    # bloco 4
    "natureza_vinculo", "atividade_prevista", "atividade_executada",
    # bloco 5
    "mecanismo", "conhecimento", "tipo_mecanismo",
    # bloco 6
    "parceiro_fluxo", "direcao_fluxo", "origem_conhecimento", "impactos",
    "limitacao_fluxo",
    # bloco 7
    "evidencia_aplicacao", "atividade_tecnologica", "funcao_associada", "descritor",
    # bloco 8
    "relacao_ct", "interpretacao_ct", "limitacao_ct",
    # bloco 12
    "informacao_adicional", "fonte_complementar",
]

# Itens da Visão geral (bloco 3), na ordem da regra de geração da especificação.
_VISAO_GERAL = [
    "id_registro", "ator_focal", "tipo_ator", "parceiros", "atividade_executada",
    "mecanismo", "evidencia_aplicacao", "relacao_ct", "status_analise",
]

_GRAUS = ["grau_atividade", "grau_mecanismo", "grau_fluxo", "grau_aplicacao", "grau_ct"]


def campo(registro: Registro, chave: str) -> str:
    """Valor do campo pronto para o relatório (com tratamento dos 3 estados)."""
    return apresentar(registro.get(chave), CAMPOS[chave].genero)


def periodo(registro: Registro, base: Base) -> str:
    """Item 1.5: período cadastrado para a fase; nunca calculado."""
    fase = como_texto(registro.get("fase_temporal")).strip()
    return base.fases.get(fase) or NAO_PREENCHIDO


def trajetoria(registro: Registro, base: Base) -> str:
    """Item 8.1: busca por Programa + Fase + Função; nunca calculada."""
    chave = tuple(
        como_texto(registro.get(k)).strip()
        for k in ("programa", "fase_temporal", "funcao_tecnologica")
    )
    return base.trajetorias.get(chave) or NAO_PREENCHIDO


def montar(registro: Registro, base: Base, agora: datetime | None = None) -> dict:
    agora = agora or datetime.now()
    c: dict = {}

    for chave in _REPRODUCAO_DIRETA:
        c[chave] = campo(registro, chave)

    # Bloco 1 — itens automáticos
    c["periodo"] = periodo(registro, base)
    c["quantidade_registros"] = "1"  # relatório individual: COUNT(IDs incluídos)
    c["data_geracao"] = agora.strftime("%d/%m/%Y — %H:%M")
    c["texto_natureza"] = textos.NATUREZA_DOCUMENTO

    # Bloco 3 — Visão geral (2 colunas)
    c["visao_geral"] = [(CAMPOS[k].rotulo, campo(registro, k)) for k in _VISAO_GERAL]

    # Blocos 4 a 8 — graus por extenso
    for g in _GRAUS:
        c[f"{g}_extenso"] = regras.grau_por_extenso(registro.get(g))

    # Bloco 4 — Leitura gerencial
    c["leitura_gerencial"] = regras.leitura_gerencial(registro.get("grau_atividade"))

    # Bloco 8 — trajetória (tabela auxiliar)
    c["trajetoria"] = trajetoria(registro, base)

    # Bloco 9 — Quadro de força + nota fixa
    c["quadro"] = regras.quadro_forca(registro.valores)
    c["nota_metodologica"] = textos.NOTA_METODOLOGICA

    # Blocos 10 e 12 — textos fixos
    c["observacao_fontes"] = textos.OBSERVACAO_FONTES
    c["condicao_preenchimento"] = textos.CONDICAO_PREENCHIMENTO

    _provisorios(c)
    return c


def _provisorios(c: dict) -> None:
    """Marcadores dos blocos das próximas etapas (E2/E3)."""
    em = textos.EM_DESENVOLVIMENTO.format
    c["resumo_executivo"] = em(n=2)
    c["fontes"] = [(em(n=10), "", "")]
    c["limitacoes"] = [(em(n=11), "")]
    c["alertas"] = em(n=11)
    for k in ("diagnostico_sugerido", "fundamento_sugestao", "diagnostico_confirmado_txt",
              "houve_alteracao", "justificativa_revisao_txt", "implicacao_gerencial"):
        c[k] = em(n=13)
    c["titulo_implicacao"] = "Implicação gerencial do diagnóstico confirmado"
    c["lacunas"] = [(em(n=14), "", "")]
    c["titulo_acao"] = "Preenchimento"
    for k in ("problema", "objetivo", "acao", "justificativa", "responsavel_potencial",
              "atores", "momento", "procedimento", "indicador", "evidencia_esperada",
              "prazo", "risco"):
        c[f"acao_{k}"] = em(n=15)
    c["conclusao"] = em(n=16)
