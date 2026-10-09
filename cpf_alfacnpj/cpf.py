from __future__ import annotations

import re

from ._normalizacao import normalizar

_CPF = re.compile(r"[0-9]{11}")


def calcular_dv1(cpf: str) -> int:
    """Cálculo do primeiro dígito verificador do CPF."""
    soma: int = sum(int(cpf[i]) * (10 - i) for i in range(9))
    return (soma * 10 % 11) % 10


def calcular_dv2(cpf: str) -> int:
    """Cálculo do segundo dígito verificador do CPF."""
    soma: int = sum(int(cpf[i]) * (11 - i) for i in range(10))
    return (soma * 10 % 11) % 10


def validar_cpf(cpf: object) -> bool:
    cpf = normalizar(cpf)

    # Exatamente 11 dígitos ASCII, sem outros caracteres
    if cpf is None or not _CPF.fullmatch(cpf):
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    return int(cpf[9]) == calcular_dv1(cpf) and int(cpf[10]) == calcular_dv2(cpf)
