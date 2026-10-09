import pytest

from cpf_alfacnpj import validar_cnpj, validar_cnpj_alfanumerico

VALIDOS_NUMERICOS = ["04.252.011/0001-10", "12.345.678/0001-95", "04252011000110"]
VALIDOS_ALFANUMERICOS = [
    "12.ABC.345/01DE-35",  # exemplo oficial da RFB
    "AB.C4A.678/0001-60",
    "12.34A.678/0001-00",
    "12.abc.345/01de-35",
    "12 ABC 345 01DE 35",
    " 12ABC34501DE35 ",
]
INVALIDOS = [
    # dígito verificador errado ou sequência repetida
    "12.345.678/0001-00",
    "00.000.000/0000-00",
    "11.111.111/1111-11",
    "AA.AAA.AAA/AAAA-00",
    "12.ABC.345/01DE-36",
    "12.ABC.678/0001-00",
    # DV não pode conter letra
    "12.345.678/0001-9a",
    "12.34A.678/0001-9Z",
    "12ABC34501DE3A",
    # caracteres inválidos
    "12.345.678/0001-@#",
    "12.345.678/0001-",
    "12.ABC.345/01DE-35!",
    "12_ABC_345_01DE_35",
    "ÇB.C4A.678/0001-60",
    "12.ABC.345/01Dß-35",
    "04.252.011/0001-1²",
    "12.ABC.345/01DE-3²",
    # tamanho incorreto
    "12.345.678/0001",
    "12.345.678/0001-1099",
    "",
]


@pytest.mark.parametrize("cnpj", VALIDOS_NUMERICOS + VALIDOS_ALFANUMERICOS)
def test_cnpj_valido(cnpj):
    assert validar_cnpj(cnpj)
    assert validar_cnpj_alfanumerico(cnpj)


@pytest.mark.parametrize("cnpj", VALIDOS_NUMERICOS)
def test_cnpj_numerico_valido(cnpj):
    assert validar_cnpj(cnpj, alfanumerico=False)


@pytest.mark.parametrize("cnpj", VALIDOS_ALFANUMERICOS)
def test_cnpj_alfanumerico_rejeitado_quando_numerico(cnpj):
    assert not validar_cnpj(cnpj, alfanumerico=False)


@pytest.mark.parametrize("cnpj", INVALIDOS)
def test_cnpj_invalido(cnpj):
    assert not validar_cnpj(cnpj)
    assert not validar_cnpj(cnpj, alfanumerico=False)
    assert not validar_cnpj_alfanumerico(cnpj)


@pytest.mark.parametrize("valor", [None, 4252011000110, b"04252011000110", ["04252011000110"], 1.5])
def test_entrada_que_nao_e_str(valor):
    assert validar_cnpj(valor) is False
    assert validar_cnpj_alfanumerico(valor) is False
