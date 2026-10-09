"""
Tipos para Pydantic v2 (``pip install "cpf-alfacnpj[pydantic]"``).

Os valores são validados e armazenados na forma limpa, sem máscara::

    from pydantic import BaseModel
    from cpf_alfacnpj.contrib.pydantic import CNPJ, CPF

    class Cliente(BaseModel):
        cpf: CPF
        cnpj_empresa: CNPJ

    Cliente(cpf="111.444.777-35", cnpj_empresa="12.ABC.345/01DE-35")
    # Cliente(cpf='11144477735', cnpj_empresa='12ABC34501DE35')
"""

from __future__ import annotations

from typing import Annotated

try:
    from pydantic import AfterValidator
except ImportError as erro:  # pragma: no cover
    raise ImportError('Esta integração requer o Pydantic v2: pip install "cpf-alfacnpj[pydantic]"') from erro

from ..cnpj import limpar_cnpj, validar_cnpj
from ..cpf import limpar_cpf, validar_cpf

__all__ = ["CNPJ", "CPF", "CNPJNumerico"]


def _cpf(valor: str) -> str:
    if not validar_cpf(valor):
        raise ValueError("CPF inválido")
    return limpar_cpf(valor)


def _cnpj(valor: str) -> str:
    if not validar_cnpj(valor):
        raise ValueError("CNPJ inválido")
    return limpar_cnpj(valor)


def _cnpj_numerico(valor: str) -> str:
    if not validar_cnpj(valor, alfanumerico=False):
        raise ValueError("CNPJ inválido (apenas CNPJ numérico é aceito)")
    return limpar_cnpj(valor)


CPF = Annotated[str, AfterValidator(_cpf)]
"""CPF válido, armazenado com 11 dígitos sem máscara."""

CNPJ = Annotated[str, AfterValidator(_cnpj)]
"""CNPJ válido (numérico ou alfanumérico), armazenado com 14 caracteres sem máscara."""

CNPJNumerico = Annotated[str, AfterValidator(_cnpj_numerico)]
"""CNPJ válido com base apenas numérica, armazenado com 14 dígitos sem máscara."""
