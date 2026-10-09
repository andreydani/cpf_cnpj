import string

from hypothesis import given
from hypothesis import strategies as st

from cpf_alfacnpj import (
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
    validar_cpf,
    validar_documento,
)

base_cpf = st.text(alphabet=string.digits, min_size=9, max_size=9).filter(lambda b: b != b[0] * 9)
base_cnpj = st.text(alphabet=string.digits + string.ascii_uppercase, min_size=12, max_size=12).filter(
    lambda b: b != b[0] * 12
)
cpf_valido = base_cpf.map(lambda b: b + calcular_dv_cpf(b))
cnpj_valido = base_cnpj.map(lambda b: b + calcular_dv_cnpj(b))


@given(st.booleans(), st.random_module())
def test_cpf_gerado_e_valido(formatado, _semente):
    cpf = gerar_cpf(formatado=formatado)
    assert validar_cpf(cpf)
    assert validar_documento(cpf)


@given(st.booleans(), st.booleans(), st.random_module())
def test_cnpj_gerado_e_valido(alfanumerico, formatado, _semente):
    cnpj = gerar_cnpj(alfanumerico=alfanumerico, formatado=formatado)
    assert validar_cnpj(cnpj)
    assert validar_documento(cnpj)


@given(cpf_valido)
def test_formatar_cpf_e_idempotente(cpf):
    formatado = formatar_cpf(cpf)
    assert formatar_cpf(limpar_cpf(formatado)) == formatado
    assert limpar_cpf(formatado) == cpf


@given(cnpj_valido)
def test_formatar_cnpj_e_idempotente(cnpj):
    formatado = formatar_cnpj(cnpj)
    assert formatar_cnpj(limpar_cnpj(formatado)) == formatado
    assert limpar_cnpj(formatado) == cnpj
    assert validar_cnpj(cnpj.lower())


@given(cpf_valido, st.integers(min_value=9, max_value=10), st.integers(min_value=1, max_value=9))
def test_alterar_dv_do_cpf_invalida(cpf, posicao, delta):
    novo = str((int(cpf[posicao]) + delta) % 10)
    assert not validar_cpf(cpf[:posicao] + novo + cpf[posicao + 1 :])


@given(cnpj_valido, st.integers(min_value=12, max_value=13), st.integers(min_value=1, max_value=9))
def test_alterar_dv_do_cnpj_invalida(cnpj, posicao, delta):
    novo = str((int(cnpj[posicao]) + delta) % 10)
    assert not validar_cnpj(cnpj[:posicao] + novo + cnpj[posicao + 1 :])


@given(st.one_of(st.text(), st.binary(), st.integers(), st.none(), st.floats()))
def test_validadores_nunca_lancam_excecao(valor):
    assert isinstance(validar_cpf(valor), bool)
    assert isinstance(validar_cnpj(valor), bool)
    assert isinstance(validar_cnpj(valor, alfanumerico=False), bool)
    assert isinstance(validar_documento(valor), bool)
    assert tipo_documento(valor) in (None, "CPF", "CNPJ")
