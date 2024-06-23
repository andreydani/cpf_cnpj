import unittest
from cpf_alfacnpj import validar_cnpj_alfanumerico as validar_cnpj


class TestValidarCNPJ(unittest.TestCase):
    def test_cnpj_valido(self):
        self.assertTrue(validar_cnpj("04.252.011/0001-10"))
        self.assertTrue(validar_cnpj("12.345.678/0001-95"))

    def test_cnpj_invalido(self):
        self.assertFalse(validar_cnpj("12.345.678/0001-00"))
        self.assertFalse(validar_cnpj("00.000.000/0000-00"))
        self.assertFalse(validar_cnpj("11.111.111/1111-11"))

    def test_cnpj_com_letras_valido(self):
        self.assertTrue(validar_cnpj("AB.C4A.678/0001-60"))  # Exemplo com letras válidas
        self.assertTrue(validar_cnpj("12.34A.678/0001-00"))  # Exemplo com letras válidas
        self.assertTrue(validar_cnpj("12.34A.678/0001-00"))  # Exemplo com letras válidas

    def test_cnpj_com_letras_invalido(self):
        self.assertFalse(validar_cnpj("12.34A.678/0001-9Z"))  # Exemplo com letras inválidas
        self.assertFalse(validar_cnpj("12.ABC.678/0001-00"))  # Exemplo com letras inválidas

    def test_cnpj_com_caracteres_invalidos(self):
        self.assertFalse(validar_cnpj("12.345.678/0001-9a"))
        self.assertFalse(validar_cnpj("12.345.678/0001-@#"))
        self.assertFalse(validar_cnpj("12.345.678/0001-"))

    def test_cnpj_com_tamanho_incorreto(self):
        self.assertFalse(validar_cnpj("12.345.678/0001"))
        self.assertFalse(validar_cnpj("12.345.678/0001-1099"))


if __name__ == "__main__":
    unittest.main()
