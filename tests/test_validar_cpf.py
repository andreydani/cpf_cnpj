import unittest
from cpf_alfacnpj import validar_cpf

class TestValidarCPF(unittest.TestCase):

    def test_cpf_valido(self):
        self.assertTrue(validar_cpf("111.444.777-35"))
        self.assertTrue(validar_cpf("123.456.789-09"))

    def test_cpf_invalido(self):
        self.assertFalse(validar_cpf("123.456.789-00"))
        self.assertFalse(validar_cpf("000.000.000-00"))
        self.assertFalse(validar_cpf("111.111.111-11"))

    def test_cpf_com_caracteres_invalidos(self):
        self.assertFalse(validar_cpf("123.456.789-0a"))
        self.assertFalse(validar_cpf("123.456.789-@#"))
        self.assertFalse(validar_cpf("123.456.789-"))

    def test_cpf_com_tamanho_incorreto(self):
        self.assertFalse(validar_cpf("123.456.789"))
        self.assertFalse(validar_cpf("123.456.789-0912"))

if __name__ == "__main__":
    unittest.main()
