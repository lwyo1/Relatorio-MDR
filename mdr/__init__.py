"""MDR-BID Digital — gerador do relatório de análise do registro.

O pacote é dividido em etapas independentes:
leitura -> estados -> regras/alertas -> montagem -> gerador.
Nenhuma etapa interpreta o conteúdo: só reproduz, converte e organiza
o que foi registrado pela pesquisadora (ver especificação funcional).
"""

__version__ = "0.1.0"
