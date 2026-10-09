"""
Geração de CPFs e CNPJs válidos para massa de testes.

Os números são aleatórios (módulo :mod:`random`) e não correspondem,
necessariamente, a pessoas ou empresas reais. Não use para fins criptográficos.
"""

from __future__ import annotations

import random
import string

from .cnpj import calcular_dv_cnpj, formatar_cnpj
from .cpf import calcular_dv_cpf, formatar_cpf

_ALFANUMERICOS = string.digits + string.ascii_uppercase


def _aleatorio(alfabeto: str, tamanho: int) -> str:
    return "".join(random.choice(alfabeto) for _ in range(tamanho))


def gerar_cpf(*, formatado: bool = False) -> str:
    """
    Gera um CPF válido aleatório.

    >>> from cpf_alfacnpj import validar_cpf
    >>> validar_cpf(gerar_cpf())
    True
    """
    while True:
        base = _aleatorio(string.digits, 9)
        if base != base[0] * 9:
            break
    cpf = base + calcular_dv_cpf(base)
    return formatar_cpf(cpf) if formatado else cpf


def gerar_cnpj(*, alfanumerico: bool = True, formatado: bool = False, filial: int = 1) -> str:
    """
    Gera um CNPJ válido aleatório.

    Por padrão a raiz (8 primeiros caracteres) é alfanumérica; use
    ``alfanumerico=False`` para gerar um CNPJ só com números. ``filial``
    define a ordem do estabelecimento (``1`` é a matriz, ``"0001"``).

    >>> from cpf_alfacnpj import validar_cnpj
    >>> validar_cnpj(gerar_cnpj())
    True
    >>> gerar_cnpj(alfanumerico=False, filial=2)[8:12]
    '0002'
    """
    if isinstance(filial, bool) or not isinstance(filial, int) or not 1 <= filial <= 9999:
        raise ValueError(f"filial deve ser um inteiro entre 1 e 9999: {filial!r}")
    alfabeto = _ALFANUMERICOS if alfanumerico else string.digits
    while True:
        base = _aleatorio(alfabeto, 8) + f"{filial:04d}"
        if base != base[0] * 12:
            break
    cnpj = base + calcular_dv_cnpj(base)
    return formatar_cnpj(cnpj) if formatado else cnpj
