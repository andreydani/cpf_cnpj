import pytest

from cpf_alfacnpj import validar_cpf


@pytest.mark.parametrize(
    "cpf",
    [
        "111.444.777-35",
        "123.456.789-09",
        "11144477735",
        "  111.444.777-35 ",
        "111 444 777 35",
        "111/444/777-35",
    ],
)
def test_cpf_valido(cpf):
    assert validar_cpf(cpf)


@pytest.mark.parametrize(
    "cpf",
    [
        # dígito verificador errado ou sequência repetida
        "123.456.789-00",
        "000.000.000-00",
        "111.111.111-11",
        "999.999.999-99",
        # caracteres inválidos
        "123.456.789-0a",
        "123.456.789-@#",
        "123.456.789-",
        "CPF 111.444.777-35",
        "111_444_777_35",
        "111.444.777-35!",
        # dígitos Unicode que não são ASCII
        "111.444.777-3²",
        "١١١٤٤٤٧٧٧٣٥",
        # tamanho incorreto
        "123.456.789",
        "123.456.789-0912",
        "",
    ],
)
def test_cpf_invalido(cpf):
    assert not validar_cpf(cpf)


@pytest.mark.parametrize("valor", [None, 11144477735, b"11144477735", ["11144477735"], 1.5])
def test_entrada_que_nao_e_str(valor):
    assert validar_cpf(valor) is False
