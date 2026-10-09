import pytest

pytest.importorskip("django")

from django import forms  # noqa: E402
from django.core.exceptions import ValidationError  # noqa: E402

from cpf_alfacnpj.contrib.django import (  # noqa: E402
    CNPJField,
    CNPJValidator,
    CPFField,
    CPFValidator,
    validar_cnpj_django,
    validar_cpf_django,
)


def test_validators_aceitam_validos():
    validar_cpf_django("111.444.777-35")
    validar_cnpj_django("12.ABC.345/01DE-35")
    CNPJValidator(alfanumerico=False)("04.252.011/0001-10")


def test_validators_rejeitam_invalidos():
    with pytest.raises(ValidationError) as erro:
        validar_cpf_django("111.444.777-36")
    assert erro.value.code == "cpf_invalido"

    with pytest.raises(ValidationError) as erro:
        CNPJValidator(alfanumerico=False)("12.ABC.345/01DE-35")
    assert erro.value.code == "cnpj_invalido"


def test_mensagem_e_code_customizados():
    with pytest.raises(ValidationError) as erro:
        CPFValidator(message="Documento ruim", code="ruim")("123")
    assert erro.value.code == "ruim"
    assert erro.value.messages == ["Documento ruim"]

    with pytest.raises(ValidationError) as erro:
        CNPJValidator(message="CNPJ ruim", code="ruim")("123")
    assert erro.value.code == "ruim"


def test_deconstruct_para_migrations():
    caminho, args, kwargs = CNPJValidator(alfanumerico=False).deconstruct()
    assert caminho == "cpf_alfacnpj.contrib.django.CNPJValidator"
    assert kwargs == {"alfanumerico": False}
    assert CNPJValidator(**kwargs) == CNPJValidator(alfanumerico=False)
    assert CNPJValidator() != CNPJValidator(alfanumerico=False)
    assert CPFValidator() == CPFValidator()
    assert CPFValidator() != CNPJValidator()
    assert len({CPFValidator(), CPFValidator()}) == 1
    assert len({CNPJValidator(), CNPJValidator(), CNPJValidator(alfanumerico=False)}) == 2


class ClienteForm(forms.Form):
    cpf = CPFField()
    cnpj = CNPJField()
    cnpj_numerico = CNPJField(alfanumerico=False, required=False)


def test_form_valido_normaliza():
    form = ClienteForm(data={"cpf": "111.444.777-35", "cnpj": "12.abc.345/01de-35", "cnpj_numerico": ""})
    assert form.is_valid(), form.errors
    assert form.cleaned_data == {"cpf": "11144477735", "cnpj": "12ABC34501DE35", "cnpj_numerico": ""}


def test_form_invalido():
    form = ClienteForm(
        data={"cpf": "111.444.777-36", "cnpj": "12.ABC.345/01DE-36", "cnpj_numerico": "12.ABC.345/01DE-35"}
    )
    assert not form.is_valid()
    assert set(form.errors) == {"cpf", "cnpj", "cnpj_numerico"}
