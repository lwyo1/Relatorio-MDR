"""Preenche o template Word (modelos/relatorio_mdr.docx) com o conteúdo montado.

Regras do template:
- {{chave}}      -> texto de conteudo["chave"], mantendo a formatação do trecho.
- {{lista.i}}    -> numa linha de tabela: a linha é repetida para cada item de
                    conteudo["lista"] (lista de tuplas), coluna i = item[i].
                    As listras das linhas (zebra) são refeitas.
Um marcador sem conteúdo correspondente é erro: nada sai com {{...}} no relatório.
"""

import copy
import re
from pathlib import Path

import docx
from docx.oxml.ns import qn

TOKEN = re.compile(r"\{\{\s*([\w]+)(?:\.(\d+))?\s*\}\}")
FUNDO_LISTRA = "EEF4F8"  # cor das linhas alternadas no modelo


class MarcadorSemConteudo(KeyError):
    pass


def _substituir_runs(paragrafo, conteudo: dict, item: tuple | None = None):
    texto_total = paragrafo.text
    if "{{" not in texto_total:
        return
    runs = paragrafo.runs
    # Se algum marcador estiver quebrado entre runs, junta tudo no primeiro run.
    if any(r.text.count("{{") != r.text.count("}}") for r in runs):
        runs[0].text = texto_total
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        runs = paragrafo.runs

    def troca(m):
        nome, idx = m.group(1), m.group(2)
        if idx is not None:
            if item is None:
                raise MarcadorSemConteudo(f"{nome}.{idx} fora de linha de tabela")
            return str(item[int(idx)])
        if nome not in conteudo:
            raise MarcadorSemConteudo(nome)
        return str(conteudo[nome])

    for r in runs:
        if "{{" in r.text:
            r.text = TOKEN.sub(troca, r.text)


def _listra(tr, ligada: bool):
    for tc in tr.iter(qn("w:tc")):
        tcPr = tc.get_or_add_tcPr()
        shd = tcPr.find(qn("w:shd"))
        if ligada:
            if shd is None:
                shd = tcPr.makeelement(qn("w:shd"), {})
                tcPr.append(shd)
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:fill"), FUNDO_LISTRA)
        elif shd is not None:
            tcPr.remove(shd)


def _lista_da_linha(row) -> str | None:
    for m in TOKEN.finditer("".join(c.text for c in row.cells)):
        if m.group(2) is not None:
            return m.group(1)
    return None


def _expandir_tabela(tabela, conteudo: dict):
    for row in list(tabela.rows):
        nome = _lista_da_linha(row)
        if nome is None:
            continue
        if nome not in conteudo:
            raise MarcadorSemConteudo(nome)
        itens = conteudo[nome]
        modelo = row._tr
        anterior = modelo
        for i, item in enumerate(itens):
            novo = copy.deepcopy(modelo)
            anterior.addnext(novo)
            anterior = novo
            _listra(novo, ligada=(i % 2 == 1))
            nova_linha = next(r for r in tabela.rows if r._tr is novo)
            for cell in nova_linha.cells:
                for p in cell.paragraphs:
                    _substituir_runs(p, conteudo, tuple(item))
        modelo.getparent().remove(modelo)


def _paragrafos(doc):
    yield from doc.paragraphs
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                yield from cell.paragraphs
    for s in doc.sections:
        yield from s.header.paragraphs
        yield from s.footer.paragraphs


def gerar(template: Path, conteudo: dict, saida: Path) -> Path:
    doc = docx.Document(str(template))
    for t in doc.tables:
        _expandir_tabela(t, conteudo)
    for p in _paragrafos(doc):
        _substituir_runs(p, conteudo)
    saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(saida))
    return saida
