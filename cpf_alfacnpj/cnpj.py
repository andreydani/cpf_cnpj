from __future__ import annotations

import re

from ._normalizacao import normalizar

_CNPJ_NUMERICO = re.compile(r"[0-9]{14}")
_CNPJ_ALFANUMERICO = re.compile(r"[0-9A-Z]{12}[0-9]{2}")


def calcular_dv1(cnpj: str) -> int:
    """
    Cálculo do primeiro dígito verificador, já preparado
    para lidar com CNPJ alfanumérico.
    """
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma: int = sum((ord(cnpj[i]) - 48) * pesos1[i] for i in range(12))
    dv1: int = 11 - (soma % 11)
    return 0 if dv1 >= 10 else dv1


def calcular_dv2(cnpj: str) -> int:
    """
    Cálculo do segundo dígito verificador, já preparado
    para lidar com CNPJ alfanumérico.
    """
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma: int = sum((ord(cnpj[i]) - 48) * pesos2[i] for i in range(13))
    dv2: int = 11 - (soma % 11)
    return 0 if dv2 >= 10 else dv2


def _validar(cnpj: object, formato: re.Pattern[str]) -> bool:
    cnpj = normalizar(cnpj)

    # Base com 12 caracteres e DV com 2 dígitos, sem outros caracteres
    if cnpj is None or not formato.fullmatch(cnpj):
        return False

    # Verifica se todos os caracteres são iguais
    if cnpj == cnpj[0] * 14:
        return False

    return int(cnpj[12]) == calcular_dv1(cnpj) and int(cnpj[13]) == calcular_dv2(cnpj)


def validar_cnpj(cnpj: object) -> bool:
    return _validar(cnpj, _CNPJ_NUMERICO)


def validar_cnpj_alfanumerico(cnpj: object) -> bool:
    return _validar(cnpj, _CNPJ_ALFANUMERICO)
