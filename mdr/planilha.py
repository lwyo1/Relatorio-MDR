"""Estrutura da planilha de entrada (contrato de dados).

Fonte única para quem CRIA a planilha (ferramentas/criar_planilha.py) e para
quem a LÊ (leitura.py). As colunas são achadas pelo nome do cabeçalho, então a
ordem das colunas pode mudar sem quebrar a leitura.
"""

from .campos import CAMPOS

# Aba principal: grupos de colunas (rótulo do grupo, chaves dos campos).
REGISTROS = "REGISTROS"
GRUPOS_REGISTROS: list[tuple[str, list[str]]] = [
    ("1. Identificação", ["id_registro", "programa", "fase_temporal",
                          "funcao_tecnologica", "ator_focal", "tipo_ator", "parceiros",
                          "status_analise", "responsavel"]),
    ("4. Vínculo e atividade", ["natureza_vinculo", "atividade_prevista",
                                "atividade_executada", "grau_atividade"]),
    ("5. Mecanismo de aprendizagem", ["mecanismo", "conhecimento", "tipo_mecanismo",
                                      "grau_mecanismo"]),
    ("6. Fluxo de conhecimento", ["parceiro_fluxo", "direcao_fluxo",
                                  "origem_conhecimento", "impactos", "grau_fluxo",
                                  "limitacao_fluxo"]),
    ("7. Aplicação tecnológica", ["evidencia_aplicacao", "atividade_tecnologica",
                                  "funcao_associada", "descritor", "grau_aplicacao"]),
    ("8. Relação com trajetória de CT", ["relacao_ct", "grau_ct", "interpretacao_ct",
                                         "limitacao_ct"]),
    ("11–12. Limitações e informação adicional", ["limitacoes_geral",
                                                  "informacao_adicional",
                                                  "fonte_complementar"]),
    ("13. Diagnóstico", ["diagnostico_confirmado", "justificativa_revisao"]),
    ("16. Conclusão", ["sintese_registro", "sintese_limitacoes"]),
]
COLUNAS_REGISTROS: list[str] = [k for _, ks in GRUPOS_REGISTROS for k in ks]
assert sorted(COLUNAS_REGISTROS) == sorted(CAMPOS), "planilha e campos.py divergem"

# Nomes alternativos aceitos no cabeçalho (nomes usados na especificação/modelo).
ALIASES = {
    "impactos": ["Impactos na acumulação de CT / manifestações observáveis"],
    "parceiros": ["Parceiro principal", "Parceiros"],
    "id_registro": ["ID MDR", "ID"],
    "programa": ["Programa/projeto", "Programa"],
}

# Abas auxiliares: nome -> [(atributo, cabeçalho)]. 1 registro -> N linhas.
FONTES = "FONTES"
LIMITACOES = "LIMITACOES"
LACUNAS = "LACUNAS"
PLANO_ACAO = "PLANO_ACAO"
FASES = "FASES"
TRAJETORIA = "TRAJETORIA"
LISTAS = "LISTAS"

CAMPOS_ACAO = [
    ("problema", "Problema diagnosticado"),
    ("objetivo", "Objetivo da ação"),
    ("acao", "Ação"),
    ("justificativa", "Justificativa/evidência"),
    ("responsavel_potencial", "Responsável potencial"),
    ("atores", "Atores envolvidos"),
    ("momento", "Momento de implementação"),
    ("procedimento", "Procedimento"),
    ("indicador", "Indicador"),
    ("evidencia_esperada", "Evidência esperada"),
    ("prazo", "Prazo de avaliação"),
    ("risco", "Risco/limitação"),
]

AUXILIARES: dict[str, list[tuple[str, str]]] = {
    FONTES: [("id_evidencia", "ID da evidência"), ("id_registro", "ID MDR"),
             ("fonte", "Fonte/Referência"), ("evidencia", "Evidência de suporte"),
             ("tipo", "Tipo de evidência")],
    LIMITACOES: [("id_limitacao", "ID da limitação"), ("id_registro", "ID MDR"),
                 ("elemento", "Elemento da limitação/indeterminação"),
                 ("situacao", "Situação identificada")],
    LACUNAS: [("id_lacuna", "ID da lacuna"), ("descricao", "Descrição da lacuna"),
              ("registros", "Registros relacionados")],
    PLANO_ACAO: [("id_acao", "ID da ação"), ("registros", "Registros relacionados"),
                 ("lacunas", "Lacunas relacionadas")] + CAMPOS_ACAO,
    FASES: [("programa", "Programa/Projeto"), ("fase", "Fase temporal"),
            ("periodo", "Período")],
    TRAJETORIA: [("programa", "Programa/Projeto"), ("fase", "Fase temporal"),
                 ("funcao", "Função tecnológica"),
                 ("trajetoria", "Trajetória/nível validado")],
}

# Listas suspensas. PROVISÓRIAS: tiradas dos exemplos dos documentos; a aluna
# confirma as opções oficiais (pergunta B6).
OPCOES: dict[str, list[str]] = {
    "Grau": ["A", "B", "C", "D", "Não aplicável"],
    "Direção do fluxo": ["Ator focal → parceiro", "Parceiro → ator focal",
                         "Bidirecional", "Multidirecional", "Não determinado"],
    "Relação com CT": ["Relação sustentada", "Relação parcialmente sustentada",
                       "Relação indeterminada", "Não aplicável"],
    "Status da análise": ["Não iniciada", "Em análise", "Pendente de evidência",
                          "Revisada", "Concluída"],
    "Tipo de ator": ["Empresa", "Universidade", "ICT", "Órgão público", "Outro"],
    "Tipo de mecanismo": ["Treinamento/capacitação", "P&D conjunto",
                          "Assistência técnica", "Execução conjunta", "Outro"],
    "Tipo de evidência": ["Documental / institucional",
                          "Documental / literatura analisada", "Entrevista",
                          "Patente", "Publicação científica", "Outro"],
    "Diagnóstico": ["I", "II", "III", "IV"],
}

# Coluna da aba principal -> lista suspensa usada.
LISTA_DA_COLUNA = {
    "grau_atividade": "Grau", "grau_mecanismo": "Grau", "grau_fluxo": "Grau",
    "grau_aplicacao": "Grau", "grau_ct": "Grau",
    "direcao_fluxo": "Direção do fluxo", "relacao_ct": "Relação com CT",
    "status_analise": "Status da análise", "tipo_ator": "Tipo de ator",
    "tipo_mecanismo": "Tipo de mecanismo", "diagnostico_confirmado": "Diagnóstico",
}
