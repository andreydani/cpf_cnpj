"""Validação, limpeza, formatação e cálculo de DV do CNPJ (numérico e alfanumérico)."""

from __future__ import annotations

import re

from ._normalizacao import normalizar

_CNPJ_NUMERICO = re.compile(r"[0-9]{14}")
_CNPJ_ALFANUMERICO = re.compile(r"[0-9A-Z]{12}[0-9]{2}")
_BASE_ALFANUMERICA = re.compile(r"[0-9A-Z]{12}")

_PESOS_DV1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_PESOS_DV2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def _dv(caracteres: str, pesos: tuple[int, ...]) -> int:
    # Cada caractere vale ord(c) - 48: '0'..'9' -> 0..9 e 'A'..'Z' -> 17..42.
    soma = sum((ord(c) - 48) * p for c, p in zip(caracteres, pesos))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def calcular_dv_cnpj(base: str) -> str:
    """
    Calcula os dois dígitos verificadores de um CNPJ a partir dos 12 primeiros caracteres.

    Aceita base numérica ou alfanumérica, com ou sem máscara.

    >>> calcular_dv_cnpj("12ABC34501DE")
    '35'
    >>> calcular_dv_cnpj("04.252.011/0001")
    '10'
    """
    limpo = normalizar(base)
    if limpo is None or not _BASE_ALFANUMERICA.fullmatch(limpo):
        raise ValueError(f"Base de CNPJ inválida (esperados 12 caracteres 0-9/A-Z): {base!r}")
    dv1 = _dv(limpo, _PESOS_DV1)
    dv2 = _dv(limpo + str(dv1), _PESOS_DV2)
    return f"{dv1}{dv2}"


def limpar_cnpj(cnpj: str) -> str:
    """
    Remove a máscara e retorna os 14 caracteres do CNPJ em maiúsculas,
    sem conferir os dígitos verificadores.

    Lança ``ValueError`` se houver caracteres inválidos ou tamanho incorreto.

    >>> limpar_cnpj("12.abc.345/01de-35")
    '12ABC34501DE35'
    """
    limpo = normalizar(cnpj)
    if limpo is None or not _CNPJ_ALFANUMERICO.fullmatch(limpo):
        raise ValueError(f"CNPJ em formato inválido: {cnpj!r}")
    return limpo


def validar_cnpj(cnpj: object, *, alfanumerico: bool = True) -> bool:
    """
    Indica se ``cnpj`` é um CNPJ válido, com ou sem máscara.

    Por padrão aceita o CNPJ alfanumérico (em vigor desde 2026). Use
    ``alfanumerico=False`` para aceitar apenas CNPJs com base numérica.
    Nunca lança exceção: qualquer entrada inválida (inclusive ``None``) retorna ``False``.

    >>> validar_cnpj("12.ABC.345/01DE-35")
    True
    >>> validar_cnpj("12.ABC.345/01DE-35", alfanumerico=False)
    False
    >>> validar_cnpj("04.252.011/0001-10", alfanumerico=False)
    True
    """
    limpo = normalizar(cnpj)
    formato = _CNPJ_ALFANUMERICO if alfanumerico else _CNPJ_NUMERICO
    if limpo is None or not formato.fullmatch(limpo):
        return False
    if limpo == limpo[0] * 14:
        return False
    return limpo[12:] == calcular_dv_cnpj(limpo[:12])


def validar_cnpj_alfanumerico(cnpj: object) -> bool:
    """
    Alias de :func:`validar_cnpj`, mantido por compatibilidade com a 0.x.

    Desde a 1.0.0, ``validar_cnpj`` já aceita o CNPJ alfanumérico por padrão.

    >>> validar_cnpj_alfanumerico("AB.C4A.678/0001-60")
    True
    """
    return validar_cnpj(cnpj)


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ válido no padrão ``00.000.000/0000-00``.

    Lança ``ValueError`` se o CNPJ for inválido.

    >>> formatar_cnpj("12abc34501de35")
    '12.ABC.345/01DE-35'
    """
    if not validar_cnpj(cnpj):
        raise ValueError(f"CNPJ inválido: {cnpj!r}")
    c = limpar_cnpj(cnpj)
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


# Mantidas por compatibilidade com a 0.x.
def calcular_dv1(cnpj: str) -> int:
    """Primeiro dígito verificador (API da 0.x; prefira :func:`calcular_dv_cnpj`)."""
    return _dv(cnpj[:12], _PESOS_DV1)


def calcular_dv2(cnpj: str) -> int:
    """Segundo dígito verificador (API da 0.x; prefira :func:`calcular_dv_cnpj`)."""
    return _dv(cnpj[:13], _PESOS_DV2)
