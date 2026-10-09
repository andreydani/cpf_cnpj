import pytest

pydantic = pytest.importorskip("pydantic")

from cpf_alfacnpj.contrib.pydantic import CNPJ, CPF, CNPJNumerico


class Cliente(pydantic.BaseModel):
    cpf: CPF
    cnpj: CNPJ


class Fornecedor(pydantic.BaseModel):
    cnpj: CNPJNumerico


def test_valores_validos_sao_normalizados():
    cliente = Cliente(cpf="111.444.777-35", cnpj="12.abc.345/01de-35")
    assert cliente.cpf == "11144477735"
    assert cliente.cnpj == "12ABC34501DE35"


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        ({"cpf": "111.444.777-36", "cnpj": "12ABC34501DE35"}, "CPF inválido"),
        ({"cpf": "11144477735", "cnpj": "12ABC34501DE36"}, "CNPJ inválido"),
        ({"cpf": None, "cnpj": "12ABC34501DE35"}, "string"),
    ],
)
def test_valores_invalidos(dados, mensagem):
    with pytest.raises(pydantic.ValidationError, match=mensagem):
        Cliente(**dados)


def test_cnpj_numerico():
    assert Fornecedor(cnpj="04.252.011/0001-10").cnpj == "04252011000110"
    with pytest.raises(pydantic.ValidationError, match="apenas CNPJ numérico"):
        Fornecedor(cnpj="12.ABC.345/01DE-35")


def test_json_schema_e_string():
    assert Cliente.model_json_schema()["properties"]["cpf"]["type"] == "string"
