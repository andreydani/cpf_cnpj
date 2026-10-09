"""Detecção automática do tipo de documento (CPF ou CNPJ)."""

from __future__ import annotations

from typing import Literal, Optional

from ._normalizacao import normalizar
from .cnpj import validar_cnpj
from .cpf import validar_cpf

TipoDocumento = Literal["CPF", "CNPJ"]


def tipo_documento(valor: object) -> Optional[TipoDocumento]:
    """
    Identifica o tipo do documento pelo tamanho, depois de remover a máscara.

    Não confere os dígitos verificadores: use :func:`validar_documento` para isso.

    >>> tipo_documento("111.444.777-35")
    'CPF'
    >>> tipo_documento("12.ABC.345/01DE-35")
    'CNPJ'
    >>> tipo_documento("123") is None
    True
    """
    limpo = normalizar(valor)
    if limpo is None:
        return None
    if len(limpo) == 11:
        return "CPF"
    if len(limpo) == 14:
        return "CNPJ"
    return None


def validar_documento(valor: object) -> bool:
    """
    Valida um CPF ou um CNPJ (numérico ou alfanumérico), detectando o tipo automaticamente.

    >>> validar_documento("111.444.777-35")
    True
    >>> validar_documento("12.ABC.345/01DE-35")
    True
    >>> validar_documento("12.ABC.345/01DE-36")
    False
    """
    tipo = tipo_documento(valor)
    if tipo == "CPF":
        return validar_cpf(valor)
    if tipo == "CNPJ":
        return validar_cnpj(valor)
    return False
