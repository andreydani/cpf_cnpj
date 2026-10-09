"""Validação, limpeza, formatação e cálculo de DV do CPF."""

from __future__ import annotations

import re

from ._normalizacao import normalizar

_CPF = re.compile(r"[0-9]{11}")
_BASE_CPF = re.compile(r"[0-9]{9}")


def _dv(digitos: str) -> int:
    peso_inicial = len(digitos) + 1
    soma = sum(int(c) * (peso_inicial - i) for i, c in enumerate(digitos))
    return soma * 10 % 11 % 10


def calcular_dv_cpf(base: str) -> str:
    """
    Calcula os dois dígitos verificadores de um CPF a partir dos 9 primeiros dígitos.

    >>> calcular_dv_cpf("111444777")
    '35'
    >>> calcular_dv_cpf("111.444.777")
    '35'
    """
    limpo = normalizar(base)
    if limpo is None or not _BASE_CPF.fullmatch(limpo):
        raise ValueError(f"Base de CPF inválida (esperados 9 dígitos): {base!r}")
    dv1 = _dv(limpo)
    dv2 = _dv(limpo + str(dv1))
    return f"{dv1}{dv2}"


def limpar_cpf(cpf: str) -> str:
    """
    Remove a máscara e retorna os 11 dígitos do CPF, sem conferir os dígitos verificadores.

    Lança ``ValueError`` se houver caracteres inválidos ou tamanho incorreto.

    >>> limpar_cpf(" 111.444.777-35 ")
    '11144477735'
    """
    limpo = normalizar(cpf)
    if limpo is None or not _CPF.fullmatch(limpo):
        raise ValueError(f"CPF em formato inválido: {cpf!r}")
    return limpo


def validar_cpf(cpf: object) -> bool:
    """
    Indica se ``cpf`` é um CPF válido, com ou sem máscara.

    Nunca lança exceção: qualquer entrada inválida (inclusive ``None``) retorna ``False``.

    >>> validar_cpf("111.444.777-35")
    True
    >>> validar_cpf("111.444.777-36")
    False
    """
    limpo = normalizar(cpf)
    if limpo is None or not _CPF.fullmatch(limpo):
        return False
    if limpo == limpo[0] * 11:
        return False
    return limpo[9:] == calcular_dv_cpf(limpo[:9])


def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF válido no padrão ``000.000.000-00``.

    Lança ``ValueError`` se o CPF for inválido.

    >>> formatar_cpf("11144477735")
    '111.444.777-35'
    """
    if not validar_cpf(cpf):
        raise ValueError(f"CPF inválido: {cpf!r}")
    c = limpar_cpf(cpf)
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"


# Mantidas por compatibilidade com a 0.x.
def calcular_dv1(cpf: str) -> int:
    """Primeiro dígito verificador (API da 0.x; prefira :func:`calcular_dv_cpf`)."""
    return _dv(cpf[:9])


def calcular_dv2(cpf: str) -> int:
    """Segundo dígito verificador (API da 0.x; prefira :func:`calcular_dv_cpf`)."""
    return _dv(cpf[:10])
