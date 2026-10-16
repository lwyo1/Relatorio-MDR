"""Caso de teste MDR-001 (Programa F-X2 Gripen).

Todo o conteúdo foi copiado do relatório-modelo preenchido do Gripen
(modelos/modelo_gripen_referencia.docx). Graus guardados só como letra,
como a especificação recomenda (item 4.4). Campos novos recomendados pela
especificação (limitação do fluxo, interpretação/limitação de CT, síntese)
recebem o texto que o modelo mostra nas caixas correspondentes.
"""

from mdr.modelos import Acao, Base, Fonte, Lacuna, Limitacao, Registro

FASE_2 = "Fase 2 — Execução e Transferência (2015–2021)"
PROGRAMA = "Programa F-X2 Gripen"
FUNCAO = "Engenharia de Manufatura"

VALORES_MDR001 = {
    "id_registro": "MDR-001",
    "programa": PROGRAMA,
    "fase_temporal": FASE_2,
    "funcao_tecnologica": FUNCAO,
    "ator_focal": "Organizações brasileiras diretamente envolvidas nas atividades "
                  "produtivas / equipes brasileiras de manufatura",
    "tipo_ator": "Organizações industriais brasileiras",
    "parceiros": "Saab AB",
    "status_analise": "Concluído para fins de aplicação demonstrativa, preservadas "
                      "as limitações registradas",
    "responsavel": "A ser identificado pelo usuário no ambiente de aplicação",
    "natureza_vinculo": "Acordo de Compensação nº 004 e Work Packages utilizados para "
                        "operacionalização da transferência de tecnologia no Programa.",
    "atividade_prevista": "Transferência de tecnologia e capacitação associadas à "
                          "execução das atividades previstas nos Work Packages de "
                          "manufatura/aeroestruturas.",
    "atividade_executada": "Capacitação teórica e prática de profissionais brasileiros "
                           "na Suécia, seguida da execução, no Brasil, de atividades de "
                           "engenharia de manufatura e produção, incluindo montagem, "
                           "testes, qualidade, logística e controle de configuração.",
    "grau_atividade": "A",
    "mecanismo": "Treinamento teórico e prático / on-the-job training, seguido de "
                 "aplicação em execução produtiva.",
    "conhecimento": "Conhecimentos e práticas relacionados à engenharia de manufatura, "
                    "montagem, testes, qualidade, logística, controle de configuração "
                    "e fabricação estrutural.",
    "tipo_mecanismo": "Treinamento/capacitação.",
    "grau_mecanismo": "A",
    "parceiro_fluxo": "Saab AB.",
    "direcao_fluxo": "Parceiro → ator focal, predominantemente.",
    "origem_conhecimento": "Saab/Suécia, para o mecanismo de capacitação analisado.",
    "impactos": "Aplicação dos conhecimentos transferidos em atividades de engenharia "
                "de manufatura e produção realizadas no Brasil.",
    "grau_fluxo": "B",
    "limitacao_fluxo": "A documentação sustenta a predominância da direção Saab → "
                       "organizações brasileiras, mas não fornece base suficiente para "
                       "caracterizar de forma generalizada os fluxos desta função como "
                       "bidirecionais ou dotados de reciprocidade simétrica.",
    "evidencia_aplicacao": "Mobilização dos conhecimentos adquiridos nas atividades de "
                           "engenharia de manufatura e produção executadas no Brasil.",
    "atividade_tecnologica": "Engenharia de manufatura e produção: montagem, testes, "
                             "qualidade, logística, controle de configuração e "
                             "fabricação estrutural, no limite das evidências "
                             "disponíveis.",
    "funcao_associada": "Engenharia de Manufatura.",
    "descritor": "Nível 5 — Inovação Avançada, como classificação da função no conjunto "
                 "das evidências da Fase 2; não como classificação individual do ator "
                 "ou deste registro isoladamente.",
    "grau_aplicacao": "A",
    "relacao_ct": "Relação parcialmente sustentada.",
    "grau_ct": "B",
    "interpretacao_ct": "A aplicação observada integra o conjunto de evidências "
                        "associado à trajetória da Engenharia de Manufatura na Fase 2, "
                        "mas o registro não permite atribuir causalmente a progressão "
                        "da função ao mecanismo de aprendizagem isolado.",
    "limitacao_ct": "A execução local de processos produtivos complexos é compatível "
                    "com o Nível 5 da função, mas não demonstra, por si só, autonomia "
                    "brasileira para redefinir parâmetros tecnológicos ou decisões "
                    "críticas de design industrial.",
    "informacao_adicional": "Registros mais específicos sobre internalização posterior, "
                            "continuidade de uso, adaptação e eventual desenvolvimento "
                            "dos conhecimentos mobilizados após a aplicação inicial nos "
                            "Work Packages.",
    "fonte_complementar": "Registros técnicos detalhados dos Work Packages, registros "
                          "de treinamento e execução, documentação técnica das "
                          "organizações envolvidas e, quando disponível, entrevistas "
                          "com participantes diretamente envolvidos.",
    "diagnostico_confirmado": "",
    "justificativa_revisao": "",
    "sintese_registro": "a passagem da capacitação teórica e prática realizada na "
                        "Suécia para a aplicação dos conhecimentos em atividades de "
                        "Engenharia de Manufatura executadas no Brasil",
    "sintese_limitacoes": "",
}

FONTES = [
    Fonte("EVD-001", "MDR-001", "Tavares (2017)",
          "Capacitação teórica e prática na Suécia; acesso aos conhecimentos e práticas "
          "necessários à execução das atividades previstas; Work Packages como "
          "referência operacional.",
          "Documental / literatura analisada"),
    Fonte("EVD-002", "MDR-001", "Correa (2026)",
          "Mobilização e aplicação dos conhecimentos em atividades produtivas; limites "
          "decisórios e proteção/compartimentação de conhecimentos críticos.",
          "Documental / literatura analisada"),
    Fonte("EVD-003", "MDR-001",
          "Documentação institucional e registros dos Work Packages analisados na "
          "pesquisa",
          "Execução de atividades de engenharia de manufatura e produção no Brasil.",
          "Documental / institucional"),
]

LIMITACOES = [
    Limitacao("LIM-001", "MDR-001", "Autonomia tecnológica",
              "Não demonstrada por este registro. A execução produtiva no Brasil não "
              "autoriza inferir autonomia para redefinir parâmetros tecnológicos "
              "associados à transferência."),
    Limitacao("LIM-002", "MDR-001", "Bidirecionalidade/reciprocidade",
              "Não caracterizável de forma generalizada para a função com as "
              "evidências deste registro."),
    Limitacao("LIM-003", "MDR-001", "Relação causal com N5",
              "Não demonstrada. A evidência integra o conjunto da trajetória da "
              "função, mas não prova causalidade."),
    Limitacao("LIM-004", "MDR-001", "Conhecimento tácito",
              "Não deve ser inferido exclusivamente a partir da documentação "
              "disponível."),
]

LACUNAS = [
    Lacuna("LAC-001", "Rastreabilidade incompleta da internalização e utilização "
           "posterior dos conhecimentos mobilizados após a aplicação inicial.",
           ["MDR-001"]),
    Lacuna("LAC-002", "Evidência insuficiente para caracterizar de forma generalizada "
           "bidirecionalidade ou reciprocidade simétrica dos fluxos na Engenharia de "
           "Manufatura.", ["MDR-001"]),
    Lacuna("LAC-003", "O registro não permite determinar desenvolvimento autônomo "
           "posterior nem atribuir causalmente a evolução da função ao mecanismo "
           "analisado.", ["MDR-001"]),
]

ACOES = [
    Acao("ACAO-001", ["MDR-001"], ["LAC-001", "LAC-002", "LAC-003"], {
        "problema": "A cadeia atividade → mecanismo → fluxo → aplicação é rastreável, "
                    "mas a internalização posterior, algumas propriedades do fluxo e a "
                    "relação com a trajetória de CT permanecem parcialmente "
                    "sustentadas.",
        "objetivo": "Aprimorar a rastreabilidade pós-aplicação dos conhecimentos "
                    "mobilizados nos Work Packages de Engenharia de Manufatura.",
        "acao": "Levantar e vincular ao registro evidências técnicas posteriores que "
                "documentem continuidade de uso, adaptação, aplicação recorrente ou "
                "desenvolvimento dos conhecimentos mobilizados.",
        "justificativa": "A documentação sustenta capacitação e aplicação produtiva, "
                         "mas não oferece base suficiente para determinar "
                         "aperfeiçoamento autônomo nem caracterizar integralmente as "
                         "propriedades do fluxo.",
        "responsavel_potencial": "A definir conforme competência institucional; "
                                 "potencialmente gestor de projeto de transferência de "
                                 "tecnologia, fiscal de offset ou unidade responsável "
                                 "pelo acompanhamento técnico.",
        "atores": "A definir conforme a localização institucional dos registros e as "
                  "competências de acesso às evidências.",
        "momento": "Pós-aplicação / acompanhamento da continuidade das capacidades; "
                   "momento específico a definir pela instituição.",
        "procedimento": "Identificar registros técnicos dos Work Packages e de "
                        "capacitação; vincular cada evidência ao ID MDR-001; verificar "
                        "continuidade, aplicação, adaptação e limites decisórios; "
                        "atualizar os graus somente mediante nova análise humana.",
        "indicador": "Existência de registros verificáveis vinculados ao MDR-001 que "
                     "reduzam as indeterminações identificadas.",
        "evidencia_esperada": "Registros técnicos, relatórios de execução, documentação "
                              "de continuidade/aplicação e outros documentos "
                              "específicos que sustentem ou mantenham como "
                              "indeterminadas as propriedades examinadas.",
        "prazo": "A definir pela instituição conforme disponibilidade das fontes e "
                 "ciclo de acompanhamento do programa.",
        "risco": "Indisponibilidade, restrição de acesso ou insuficiente especificidade "
                 "dos registros; ausência documental não deve ser interpretada "
                 "automaticamente como ausência de aprendizagem ou contribuição "
                 "tecnológica.",
    }),
]


def base_gripen() -> Base:
    return Base(
        registros=[Registro(dict(VALORES_MDR001))],
        fontes=list(FONTES),
        limitacoes=list(LIMITACOES),
        lacunas=list(LACUNAS),
        acoes=list(ACOES),
        fases={FASE_2: "2015–2021"},
        trajetorias={(PROGRAMA, FASE_2, FUNCAO):
                     "Engenharia de Manufatura: Nível 5 — Inovação Avançada, no "
                     "conjunto de evidências da fase."},
    )
