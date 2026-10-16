"""Textos fixos e frases-modelo do relatório.

Todos os textos vêm da especificação funcional (citada em cada constante).
Mudar uma redação = mudar aqui, em um só lugar.
"""

# Caixa "Natureza deste documento" (topo do relatório).
# O modelo genérico traz este texto como instrução entre colchetes; aqui ele foi
# passado para a voz descritiva, sem mudar o conteúdo. REDAÇÃO A VALIDAR COM A ALUNA.
NATUREZA_DOCUMENTO = (
    "Relatório padronizado gerado a partir do preenchimento da MDR-BID Digital "
    "para o registro analisado. O relatório apresenta somente informações "
    "registradas, classificadas ou validadas no sistema. Quando uma propriedade "
    "não pôde ser determinada pelas evidências disponíveis, ela é apresentada como "
    "“Não determinado”, “Indeterminado” ou “A definir”, "
    "conforme o campo, sem preenchimento inferencial."
)

# Bloco 4 — Leitura gerencial (especificação, item 4.5 / regra de geração).
LEITURA_GERENCIAL_FIXA = (
    "A atividade prevista e a atividade executada/documentada foram analisadas "
    "separadamente, de modo que a previsão da atividade não constitui, por si só, "
    "evidência de sua execução."
)
LEITURA_GERENCIAL_POR_GRAU = {
    "A": "Para este registro, a execução da atividade descrita encontra-se "
         "sustentada pelas evidências registradas.",
    "B": "Para este registro, a execução da atividade descrita encontra-se "
         "parcialmente sustentada pelas evidências registradas, permanecendo "
         "aspectos que não puderam ser plenamente determinados.",
    "C": "Para este registro, as evidências sustentam a participação ou o vínculo "
         "entre os atores, mas não permitem sustentar suficientemente a execução "
         "da atividade descrita.",
    "D": "Para este registro, as evidências disponíveis são insuficientes para "
         "determinar a execução da atividade.",
}

# Bloco 9 — nota abaixo do quadro (item 9.8).
NOTA_METODOLOGICA = (
    "os graus A–D qualificam afirmações ou propriedades específicas. Não constituem "
    "nota geral, medida de desempenho, indicador de sucesso da transferência de "
    "tecnologia ou nível automático de capacidade tecnológica."
)

# Bloco 10 — observação abaixo da tabela (item 10.7, versão genérica).
OBSERVACAO_FONTES = (
    "As fontes e evidências apresentadas neste quadro correspondem às informações "
    "registradas e validadas na MDR-BID. O relatório não acrescenta referências "
    "externas, não completa automaticamente dados bibliográficos ausentes e não "
    "produz novas evidências a partir das fontes cadastradas."
)

# Bloco 12 — condição de preenchimento (item 12.4, versão genérica).
CONDICAO_PREENCHIMENTO = (
    "Quando a informação adicional necessária não estiver disponível ou as fontes "
    "consultadas não permitirem determinar suficientemente a propriedade examinada, "
    "a condição deverá permanecer registrada como indeterminada, sem inferência "
    "automática."
)

# Marcador provisório para blocos ainda não implementados nesta etapa.
EM_DESENVOLVIMENTO = "[Em desenvolvimento — bloco {n}]"
