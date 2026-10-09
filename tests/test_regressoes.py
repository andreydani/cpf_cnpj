import unittest

from cpf_alfacnpj import validar_cnpj, validar_cnpj_alfanumerico, validar_cpf


class TestRegressoes(unittest.TestCase):
    def test_digitos_unicode_nao_lancam_excecao(self):
        self.assertFalse(validar_cpf("111.444.777-3²"))
        self.assertFalse(validar_cnpj("04.252.011/0001-1²"))
        self.assertFalse(validar_cnpj_alfanumerico("12.ABC.345/01DE-3²"))
        self.assertFalse(validar_cpf("١١١٤٤٤٧٧٧٣٥"))  # dígitos arábicos

    def test_letras_fora_do_ascii(self):
        self.assertFalse(validar_cnpj_alfanumerico("ÇB.C4A.678/0001-60"))
        self.assertFalse(validar_cnpj_alfanumerico("12.ABC.345/01Dß-35"))

    def test_entrada_que_nao_e_str(self):
        for valor in (None, 11144477735, 4252011000110, b"11144477735", ["1"]):
            self.assertFalse(validar_cpf(valor))
            self.assertFalse(validar_cnpj(valor))
            self.assertFalse(validar_cnpj_alfanumerico(valor))

    def test_caracteres_extras_invalidam(self):
        self.assertFalse(validar_cpf("CPF 111.444.777-35"))
        self.assertFalse(validar_cpf("111_444_777_35"))
        self.assertFalse(validar_cnpj_alfanumerico("12.ABC.345/01DE-35!"))

    def test_mascara_e_espacos_sao_aceitos(self):
        self.assertTrue(validar_cpf("  111.444.777-35 "))
        self.assertTrue(validar_cnpj_alfanumerico("12 ABC 345 01DE 35"))
        self.assertTrue(validar_cnpj_alfanumerico("12.abc.345/01de-35"))

    def test_dv_alfanumerico_nao_pode_conter_letra(self):
        self.assertFalse(validar_cnpj_alfanumerico("12ABC34501DE3A"))


if __name__ == "__main__":
    unittest.main()
