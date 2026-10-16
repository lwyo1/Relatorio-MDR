import unittest
from datetime import datetime

from mdr.estados import (
    NAO_APLICAVEL_TEXTO, NAO_PREENCHIDO, Estado, apresentar, classificar, como_texto,
)


class TestClassificar(unittest.TestCase):
    def test_vazio(self):
        for v in (None, "", "   ", "\n"):
            self.assertIs(classificar(v), Estado.VAZIO, repr(v))

    def test_nao_determinado_variacoes(self):
        for v in ("Não determinado", "não determinada", "NAO DETERMINADOS",
                  "Não determinadas.", " Não  determinado ",
                  "Não determinado com as evidências disponíveis"):
            self.assertIs(classificar(v), Estado.NAO_DETERMINADO, v)

    def test_nao_aplicavel_variacoes(self):
        for v in ("Não aplicável", "nao aplicavel", "Não aplicável ao registro analisado."):
            self.assertIs(classificar(v), Estado.NAO_APLICAVEL, v)

    def test_texto_livre_nao_e_estado(self):
        # Conteúdo da pesquisadora que só começa com a expressão é reproduzido.
        for v in ("Não determinado por este registro; ver LAC-002.",
                  "Relação indeterminada",   # categoria válida da Relação com CT
                  "Indeterminado",           # não é uma das formas da matriz
                  "Não demonstrada por este registro."):
            self.assertIs(classificar(v), Estado.PREENCHIDO, v)


class TestApresentar(unittest.TestCase):
    def test_concordancia_de_genero(self):
        self.assertEqual(apresentar("Não determinado", "m"),
                         "Não determinado com as evidências disponíveis")
        self.assertEqual(apresentar("Não determinado", "f"),
                         "Não determinada com as evidências disponíveis")
        self.assertEqual(apresentar("não determinada", "fp"),
                         "Não determinadas com as evidências disponíveis")

    def test_nao_aplicavel(self):
        self.assertEqual(apresentar("Não aplicável", "f"), NAO_APLICAVEL_TEXTO)

    def test_vazio_nunca_vira_nao_determinado(self):
        self.assertEqual(apresentar(None, "f"), NAO_PREENCHIDO)
        self.assertEqual(apresentar("  ", "m"), NAO_PREENCHIDO)

    def test_reproducao_literal(self):
        texto = "Saab AB; Organização X; Organização Y."
        self.assertEqual(apresentar(texto), texto)

    def test_valores_nao_texto(self):
        self.assertEqual(como_texto(3.0), "3")
        self.assertEqual(como_texto(datetime(2026, 10, 15)), "15/10/2026")


if __name__ == "__main__":
    unittest.main()
