import pytest

from cpf_alfacnpj import (
    __version__,
    calcular_dv_cnpj,
    calcular_dv_cpf,
    formatar_cnpj,
    formatar_cpf,
    gerar_cnpj,
    gerar_cpf,
    limpar_cnpj,
    limpar_cpf,
    tipo_documento,
    validar_cnpj,
    validar_cnpj_alfanumerico,
    validar_cpf,
    validar_documento,
)
from cpf_alfacnpj import cnpj as modulo_cnpj
from cpf_alfacnpj import cpf as modulo_cpf


def test_versao():
    assert __version__ == "1.0.0"


@pytest.mark.parametrize(
    ("base", "dv"),
    [("111444777", "35"), ("123456789", "09"), ("111.444.777", "35")],
)
def test_calcular_dv_cpf(base, dv):
    assert calcular_dv_cpf(base) == dv


@pytest.mark.parametrize(
    ("base", "dv"),
    [
        ("12ABC34501DE", "35"),
        ("12.abc.345/01de", "35"),
        ("042520110001", "10"),
        ("123456780001", "95"),
        ("ABC4A6780001", "60"),
    ],
)
def test_calcular_dv_cnpj(base, dv):
    assert calcular_dv_cnpj(base) == dv


@pytest.mark.parametrize("base", ["", "11144477", "1114447770", "11144477A", None])
def test_calcular_dv_cpf_base_invalida(base):
    with pytest.raises(ValueError):
        calcular_dv_cpf(base)


@pytest.mark.parametrize("base", ["", "12ABC34501D", "12ABC34501DE3", "12ABC34501D!", "12ÇBC34501DE", None])
def test_calcular_dv_cnpj_base_invalida(base):
    with pytest.raises(ValueError):
        calcular_dv_cnpj(base)


def test_limpar():
    assert limpar_cpf(" 111.444.777-35 ") == "11144477735"
    assert limpar_cnpj("12.abc.345/01de-35") == "12ABC34501DE35"
    # limpar não confere DV
    assert limpar_cpf("111.444.777-00") == "11144477700"
    assert limpar_cnpj("12.ABC.345/01DE-00") == "12ABC34501DE00"


@pytest.mark.parametrize("valor", ["111.444.777", "111.444.777-3a", "CPF 11144477735", None])
def test_limpar_cpf_invalido(valor):
    with pytest.raises(ValueError):
        limpar_cpf(valor)


@pytest.mark.parametrize("valor", ["12.ABC.345/01DE", "12.ABC.345/01DE-3A", "12.ABC.345/01DE-35!", None])
def test_limpar_cnpj_invalido(valor):
    with pytest.raises(ValueError):
        limpar_cnpj(valor)


def test_formatar():
    assert formatar_cpf("11144477735") == "111.444.777-35"
    assert formatar_cpf("111.444.777-35") == "111.444.777-35"
    assert formatar_cnpj("12abc34501de35") == "12.ABC.345/01DE-35"
    assert formatar_cnpj("04252011000110") == "04.252.011/0001-10"


@pytest.mark.parametrize("valor", ["11144477736", "11111111111", "abc"])
def test_formatar_cpf_invalido(valor):
    with pytest.raises(ValueError):
        formatar_cpf(valor)


@pytest.mark.parametrize("valor", ["12ABC34501DE36", "00000000000000", "abc"])
def test_formatar_cnpj_invalido(valor):
    with pytest.raises(ValueError):
        formatar_cnpj(valor)


def test_validar_cnpj_aceita_alfanumerico_por_padrao():
    assert validar_cnpj("12.ABC.345/01DE-35")
    assert validar_cnpj("AB.C4A.678/0001-60")
    assert not validar_cnpj("12.ABC.345/01DE-35", alfanumerico=False)
    assert validar_cnpj("04.252.011/0001-10", alfanumerico=False)
    assert not validar_cnpj("AAAAAAAAAAAAAA")


def test_alias_alfanumerico():
    assert validar_cnpj_alfanumerico("12.ABC.345/01DE-35")
    assert not validar_cnpj_alfanumerico("12.ABC.345/01DE-36")


@pytest.mark.parametrize(
    ("valor", "tipo", "valido"),
    [
        ("111.444.777-35", "CPF", True),
        ("111.444.777-36", "CPF", False),
        ("12.ABC.345/01DE-35", "CNPJ", True),
        ("04.252.011/0001-10", "CNPJ", True),
        ("04.252.011/0001-11", "CNPJ", False),
        ("123", None, False),
        ("", None, False),
        (None, None, False),
        ("111.444.777-3²", None, False),
    ],
)
def test_documento(valor, tipo, valido):
    assert tipo_documento(valor) == tipo
    assert validar_documento(valor) is valido


def test_gerar_cpf():
    for _ in range(200):
        cpf = gerar_cpf()
        assert len(cpf) == 11 and validar_cpf(cpf)
    assert validar_cpf(gerar_cpf(formatado=True))
    assert gerar_cpf(formatado=True)[3] == "."


def test_gerar_cnpj():
    for _ in range(200):
        assert validar_cnpj(gerar_cnpj())
        numerico = gerar_cnpj(alfanumerico=False)
        assert numerico.isdigit() and validar_cnpj(numerico, alfanumerico=False)
    assert gerar_cnpj()[8:12] == "0001"
    assert gerar_cnpj(filial=42)[8:12] == "0042"
    assert gerar_cnpj(formatado=True)[2] == "."


@pytest.mark.parametrize("filial", [0, 10000, -1, True, "1", 1.0])
def test_gerar_cnpj_filial_invalida(filial):
    with pytest.raises(ValueError):
        gerar_cnpj(filial=filial)


def test_gerar_evita_sequencias_repetidas(monkeypatch):
    escolhas = iter(["1"] * 9 + list("111444777"))
    monkeypatch.setattr("cpf_alfacnpj.gerador.random.choice", lambda _: next(escolhas))
    assert gerar_cpf() == "11144477735"

    escolhas_cnpj = iter(list("11111111") + list("12ABC345"))
    monkeypatch.setattr("cpf_alfacnpj.gerador.random.choice", lambda _: next(escolhas_cnpj))
    assert gerar_cnpj(filial=1111) == "12ABC3451111" + calcular_dv_cnpj("12ABC3451111")


def test_api_0x_compativel():
    assert modulo_cpf.calcular_dv1("111444777") == 3
    assert modulo_cpf.calcular_dv2("1114447773") == 5
    assert modulo_cnpj.calcular_dv1("12ABC34501DE") == 3
    assert modulo_cnpj.calcular_dv2("12ABC34501DE3") == 5
