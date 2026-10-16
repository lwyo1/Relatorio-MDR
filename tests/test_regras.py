import unittest

from mdr import regras, textos
from mdr.estados import NAO_APLICAVEL_TEXTO, NAO_PREENCHIDO


class TestLeituraDoGrau(unittest.TestCase):
    def test_formas_aceitas(self):
        for v in ("A", "a", " B ", "C — Participação ou vínculo documentado",
                  "D - Evidência insuficiente", "A.", "B: parcialmente"):
            self.assertIn(regras.ler_grau(v).codigo, "ABCD", v)

    def test_grau_invalido_e_sinalizado(self):
        for v in ("E", "Alto", "AB", "5"):
            g = regras.ler_grau(v)
            self.assertIsNone(g.codigo, v)
            self.assertFalse(g.valido, v)

    def test_por_extenso(self):
        self.assertEqual(regras.grau_por_extenso("A"), "A — Evidência sustentada")
        self.assertEqual(regras.grau_por_extenso("b"),
                         "B — Evidência parcialmente sustentada")
        self.assertEqual(regras.grau_por_extenso("C"),
                         "C — Participação ou vínculo documentado")
        self.assertEqual(regras.grau_por_extenso("D"), "D — Evidência insuficiente")


class TestQuadroDeForca(unittest.TestCase):
    def test_cinco_linhas_fixas_sem_agregado(self):
        q = regras.quadro_forca({"grau_atividade": "A", "grau_mecanismo": "A",
                                 "grau_fluxo": "B", "grau_aplicacao": "A",
                                 "grau_ct": "B"})
        self.assertEqual([l[0] for l in q], [
            "Atividade executada", "Mecanismo de aprendizagem",
            "Fluxo de conhecimento", "Aplicação tecnológica",
            "Relação com trajetória de CT"])
        self.assertEqual([l[1] for l in q], ["A", "A", "B", "A", "B"])
        # Nenhuma linha extra de "grau geral", média ou total (item 9.7).
        self.assertEqual(len(q), 5)

    def test_vazio_nao_aplicavel_e_nao_determinado_nunca_viram_D(self):
        q = regras.quadro_forca({"grau_atividade": None,
                                 "grau_mecanismo": "Não aplicável",
                                 "grau_fluxo": "Não determinado",
                                 "grau_aplicacao": "", "grau_ct": "D"})
        self.assertEqual(q[0][1:], ("—", NAO_PREENCHIDO))
        self.assertEqual(q[1][1:], ("—", NAO_APLICAVEL_TEXTO))
        self.assertEqual(q[2][1], "—")
        self.assertEqual(q[3][1:], ("—", NAO_PREENCHIDO))
        self.assertEqual(q[4][1:], ("D", "Evidência insuficiente"))


class TestLeituraGerencial(unittest.TestCase):
    def test_frase_fixa_mais_frase_do_grau(self):
        for g in "ABCD":
            texto = regras.leitura_gerencial(g)
            self.assertTrue(texto.startswith(textos.LEITURA_GERENCIAL_FIXA))
            self.assertTrue(texto.endswith(textos.LEITURA_GERENCIAL_POR_GRAU[g]))

    def test_sem_grau_fica_so_a_frase_fixa(self):
        self.assertEqual(regras.leitura_gerencial(None), textos.LEITURA_GERENCIAL_FIXA)


if __name__ == "__main__":
    unittest.main()
