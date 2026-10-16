"""Catálogo dos campos de um registro MDR-BID.

Cada campo tem:
- rotulo: nome exibido no relatório e nos alertas;
- genero: concordância usada em "Não determinad[o|a|os|as] com as evidências
  disponíveis" (m, f, mp, fp), conforme os exemplos da especificação;
- grau: True para os cinco campos de grau A–D.

A chave (ex.: "atividade_executada") é o nome interno usado em todo o código.
O vínculo com as colunas da planilha fica em leitura.py, num único lugar.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Campo:
    chave: str
    rotulo: str
    genero: str = "m"
    grau: bool = False


_LISTA = [
    # Bloco 1 — Identificação
    Campo("id_registro", "ID do registro"),
    Campo("programa", "Programa/Projeto"),
    Campo("fase_temporal", "Fase temporal", "f"),
    Campo("funcao_tecnologica", "Função tecnológica", "f"),
    Campo("ator_focal", "Ator focal"),
    Campo("tipo_ator", "Tipo de ator"),
    Campo("parceiros", "Parceiro(s)"),
    Campo("status_analise", "Status da análise"),
    Campo("responsavel", "Responsável pela análise"),
    # Bloco 4 — Vínculo e atividade
    Campo("natureza_vinculo", "Natureza do vínculo/formalização"),
    Campo("atividade_prevista", "Atividade prevista", "f"),
    Campo("atividade_executada", "Atividade executada/documentada", "f"),
    Campo("grau_atividade", "Grau — atividade executada", grau=True),
    # Bloco 5 — Mecanismo de aprendizagem
    Campo("mecanismo", "Mecanismo de aprendizagem observado"),
    Campo("conhecimento", "Conhecimento mobilizado"),
    Campo("tipo_mecanismo", "Tipo de mecanismo para análise da variedade"),
    Campo("grau_mecanismo", "Grau — mecanismo de aprendizagem", grau=True),
    # Bloco 6 — Fluxo de conhecimento
    Campo("parceiro_fluxo", "Parceiro do fluxo"),
    Campo("direcao_fluxo", "Direção do fluxo"),
    Campo("origem_conhecimento", "Origem do conhecimento", "f"),
    Campo("impactos", "Impactos / manifestações observáveis", "fp"),
    Campo("grau_fluxo", "Grau — fluxo de conhecimento", grau=True),
    Campo("limitacao_fluxo", "Limitação — fluxo de conhecimento", "f"),
    # Bloco 7 — Aplicação tecnológica
    Campo("evidencia_aplicacao", "Evidência de aplicação tecnológica", "f"),
    Campo("atividade_tecnologica", "Atividade tecnológica associada", "f"),
    Campo("funcao_associada", "Função tecnológica associada", "f"),
    Campo("descritor", "Descritor taxonômico"),
    Campo("grau_aplicacao", "Grau — aplicação tecnológica", grau=True),
    # Bloco 8 — Relação com trajetória de CT
    Campo("relacao_ct", "Relação com trajetória de CT da função", "f"),
    Campo("grau_ct", "Grau — relação com trajetória de CT", grau=True),
    Campo("interpretacao_ct", "Interpretação da relação com trajetória de CT", "f"),
    Campo("limitacao_ct", "Limitação — relação com trajetória de CT", "f"),
    # Bloco 11 / 12
    Campo("limitacoes_geral", "Limitações", "fp"),
    Campo("informacao_adicional", "Informação adicional necessária", "f"),
    Campo("fonte_complementar", "Fonte complementar recomendada", "f"),
    # Bloco 13
    Campo("diagnostico_confirmado", "Diagnóstico confirmado pelo responsável"),
    Campo("justificativa_revisao", "Justificativa da revisão", "f"),
    # Bloco 16 (campos de síntese recomendados pela especificação)
    Campo("sintese_registro", "Síntese do registro para conclusão", "f"),
    Campo("sintese_limitacoes", "Síntese das limitações para conclusão", "f"),
]

CAMPOS: dict[str, Campo] = {c.chave: c for c in _LISTA}

# Os cinco graus, na ordem fixa do Quadro de força das evidências (bloco 9).
DIMENSOES_GRAU: list[tuple[str, str]] = [
    ("Atividade executada", "grau_atividade"),
    ("Mecanismo de aprendizagem", "grau_mecanismo"),
    ("Fluxo de conhecimento", "grau_fluxo"),
    ("Aplicação tecnológica", "grau_aplicacao"),
    ("Relação com trajetória de CT", "grau_ct"),
]
