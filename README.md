# Relatório MDR-BID Digital

Gera o relatório de análise de um registro MDR-BID (16 blocos, formato Word)
a partir dos dados preenchidos pela pesquisadora. O sistema só reproduz,
converte e organiza o que foi registrado; não interpreta nem completa dados.

## Estrutura

```
mdr/                núcleo, sem interface
  campos.py         catálogo dos campos (rótulo, concordância, graus)
  estados.py        Não determinado / Não aplicável / vazio
  regras.py         graus A–D, quadro de força, leitura gerencial
  textos.py         textos fixos e frases-modelo da especificação
  modelos.py        estrutura interna (Registro, Fonte, Limitação, Lacuna, Ação)
  planilha.py       estrutura da planilha de entrada (abas, colunas, listas)
  leitura.py        lê a planilha pelo nome das colunas e monta a Base
  montagem.py       conteúdo de cada bloco do relatório
  gerador.py        preenche o template Word
gerar_relatorio.py  gera o relatório de um registro a partir da planilha
modelos/
  planilha_mdr.xlsx             planilha de entrada, com o MDR-001 de exemplo
  relatorio_mdr.docx            template com marcadores {{...}}
  modelo_gripen_referencia.docx relatório-modelo do Gripen (referência visual e de teste)
ferramentas/
  criar_planilha.py recria a planilha de entrada a partir de mdr/planilha.py
  criar_template.py recria o template a partir do modelo do Gripen
  gerar_gripen.py   gera o relatório do caso de teste direto dos dados de teste
tests/              testes automatizados (unittest)
```

## Comandos

```
python gerar_relatorio.py modelos/planilha_mdr.xlsx MDR-001   # gera saida/Relatorio_MDR-001.docx
python -m unittest discover -s tests -t .                     # roda os testes
python ferramentas/criar_planilha.py                          # recria a planilha de entrada
python ferramentas/criar_template.py                          # recria o template
```

Dependências: Python 3.11+, `python-docx`, `openpyxl`.

## Planilha de entrada

| Aba | Uma linha = |
| --- | --- |
| REGISTROS | um registro MDR (39 colunas, agrupadas pelos blocos do relatório) |
| FONTES | uma evidência ligada a um registro pelo ID MDR |
| LIMITACOES | uma limitação/indeterminação de um registro |
| LACUNAS | uma lacuna, com os registros relacionados separados por `;` |
| PLANO_ACAO | uma ação, com registros e lacunas relacionados |
| FASES | o período de uma fase de um programa |
| TRAJETORIA | a trajetória validada de uma função por programa e fase |
| LISTAS | opções das listas suspensas (provisórias) |

Escreva exatamente "Não determinado" ou "Não aplicável" quando for o caso;
célula vazia significa "ainda não preenchido" e gera alerta.

## Situação (E1, 15/10/2026)

Prontos: planilha de entrada, leitura, e os blocos 1, 3, 4, 5, 6, 7, 8, 9 e 12,
com teste de ouro contra o modelo do Gripen. Os demais blocos aparecem como
"[Em desenvolvimento — bloco N]".
