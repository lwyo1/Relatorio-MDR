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
  montagem.py       conteúdo de cada bloco do relatório
  gerador.py        preenche o template Word
modelos/
  relatorio_mdr.docx            template com marcadores {{...}}
  modelo_gripen_referencia.docx relatório-modelo do Gripen (referência visual e de teste)
ferramentas/
  criar_template.py gera o template a partir do modelo do Gripen
  gerar_gripen.py   gera o relatório do caso de teste MDR-001
tests/              testes automatizados (unittest)
```

## Comandos

```
python ferramentas/criar_template.py      # recria o template
python ferramentas/gerar_gripen.py        # gera saida/Relatorio_MDR-001.docx
python -m unittest discover -s tests -t . # roda os testes
```

Dependências: Python 3.11+, `python-docx`, `openpyxl`.

## Situação (E1, 15/10/2026)

Prontos: blocos 1, 3, 4, 5, 6, 7, 8, 9 e 12, com teste de ouro contra o modelo
do Gripen. Os demais blocos aparecem como "[Em desenvolvimento — bloco N]".
